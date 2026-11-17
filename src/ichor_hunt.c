// Artemis's grove: patrolling hounds see farther in the moonlit clearings.
#include "global.h"
#include "event_data.h"
#include "field_control_avatar.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "ichor_hunt.h"
#include "main.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/layouts.h"
#include "constants/map_event_ids.h"
#include "constants/vars.h"

extern const u8 Arkadia_TempleOfArtemis_EventScript_Caught[];

static const struct { u8 localId, stage; } sHounds[] =
{
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDTEACH, 0},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDTEST1, 1},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDTEST2, 1},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDTEST3, 1},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDMASTER1, 2},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDMASTER2, 2},
    {LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDMASTER3, 2},
};

static bool32 IsMoonlit(s16 x, s16 y)
{
    x -= MAP_OFFSET;
    y -= MAP_OFFSET;
    // The grove's three pale clearings (layouts/Arkadia_TempleOfArtemis, from world-act2):
    // two in the second glade, one in the third.
    return (x >= 4 && x <= 11 && y >= 23 && y <= 26)
        || (x >= 18 && x <= 25 && y >= 24 && y <= 29)
        || (x >= 21 && x <= 26 && y >= 8 && y <= 13);
}

static bool32 SeesPlayer(const struct ObjectEvent *hound, s16 px, s16 py)
{
    static const s8 dx[] = {0, 0, 0, -1, 1};
    static const s8 dy[] = {0, 1, -1, 0, 0};
    s16 x = hound->currentCoords.x, y = hound->currentCoords.y;
    u32 direction = hound->facingDirection;
    u32 distance, range = IsMoonlit(px, py) ? 6 : 3;

    if (direction < DIR_SOUTH || direction > DIR_EAST)
        return FALSE;
    for (distance = 1; distance <= range; distance++)
    {
        x += dx[direction];
        y += dy[direction];
        if (MapGridGetCollisionAt(x, y))
            return FALSE;
        if (x == px && y == py)
            return TRUE;
    }
    return FALSE;
}

void Ichor_HuntFrame(void)
{
    struct ObjectEvent *player;
    u32 i, h, stage;

    if (gMapHeader.mapLayoutId != LAYOUT_ARKADIA_TEMPLE_OF_ARTEMIS
     || gMain.callback2 != CB2_Overworld || gPaletteFade.active
     || ScriptContext_IsEnabled() || ArePlayerFieldControlsLocked()
     || gPlayerAvatar.objectEventId >= OBJECT_EVENTS_COUNT
     || gPlayerAvatar.tileTransitionState == T_TILE_TRANSITION
     || FlagGet(FLAG_ICHOR_KALLISTO_TRIAL))
        return;
    player = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (!player->active)
        return;
    stage = VarGet(VAR_ICHOR_HUNT_STAGE);
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *hound = &gObjectEvents[i];
        if (!hound->active || hound->invisible
         || hound->mapGroup != gSaveBlock1Ptr->location.mapGroup
         || hound->mapNum != gSaveBlock1Ptr->location.mapNum)
            continue;
        for (h = 0; h < ARRAY_COUNT(sHounds); h++)
        {
            if (hound->localId == sHounds[h].localId && stage == sHounds[h].stage
             && SeesPlayer(hound, player->currentCoords.x, player->currentCoords.y))
            {
                ScriptContext_SetupScript(Arkadia_TempleOfArtemis_EventScript_Caught);
                LockPlayerFieldControls();
                return;
            }
        }
    }
}
