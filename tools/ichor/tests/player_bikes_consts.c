#include "elaia_effects_consts.c"

K(GFX_THEO_MACH, OBJ_EVENT_GFX_BRENDAN_MACH_BIKE)
K(GFX_IANTHE_MACH, OBJ_EVENT_GFX_MAY_MACH_BIKE)
K(GFX_THEO_ACRO, OBJ_EVENT_GFX_BRENDAN_ACRO_BIKE)
K(GFX_IANTHE_ACRO, OBJ_EVENT_GFX_MAY_ACRO_BIKE)
K(GFX_RIVAL_THEO_MACH, OBJ_EVENT_GFX_RIVAL_BRENDAN_MACH_BIKE)
K(GFX_RIVAL_IANTHE_MACH, OBJ_EVENT_GFX_RIVAL_MAY_MACH_BIKE)
K(GFX_RIVAL_THEO_ACRO, OBJ_EVENT_GFX_RIVAL_BRENDAN_ACRO_BIKE)
K(GFX_RIVAL_IANTHE_ACRO, OBJ_EVENT_GFX_RIVAL_MAY_ACRO_BIKE)
K(FRAME_IMAGE_SIZE, sizeof(struct SpriteFrameImage))
K(ANIM_STD_COUNT, ANIM_STD_COUNT)

bool8 PlayerBikes_Setup(struct ScriptContext *ctx)
{
    // Quickstart identity is randomized; fix only this test's walking observer.
    gSaveBlock2Ptr->playerGender = 0;
    gPlayerAvatar.gender = 0;
    ObjectEventSetGraphicsId(&gObjectEvents[gPlayerAvatar.objectEventId],
                             OBJ_EVENT_GFX_BRENDAN_NORMAL);
    return FALSE;
}
