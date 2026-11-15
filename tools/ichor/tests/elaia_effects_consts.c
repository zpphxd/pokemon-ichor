#include "engine_consts.h"
#include "sprite.h"
#include "script.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_effect.h"
#include "field_effect_helpers.h"
#include "field_camera.h"
#include "field_weather.h"
#include "field_player_avatar.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/field_effects.h"
#include "constants/opponents.h"
#include "constants/species.h"

K(SPRITE_SIZE, sizeof(struct Sprite))
K(SPRITE_LIMIT, MAX_SPRITES)
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_IMAGES, offsetof(struct Sprite, images))
K(OFF_SPRITE_ANIMS, offsetof(struct Sprite, anims))
K(OFF_SPRITE_ANIM_NUM, offsetof(struct Sprite, animNum))
K(OFF_SPRITE_ANIM_CMD, offsetof(struct Sprite, animCmdIndex))
K(OFF_SPRITE_DATA, offsetof(struct Sprite, data))
K(OFF_SPRITE_FLAGS, offsetof(struct Sprite, sheetTileStart) - sizeof(u16))
K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(GFX_THEO_FISH, OBJ_EVENT_GFX_BRENDAN_FISHING)
K(GFX_IANTHE_FISH, OBJ_EVENT_GFX_MAY_FISHING)
K(GFX_THEO_SURF, OBJ_EVENT_GFX_BRENDAN_SURFING)
K(GFX_IANTHE_SURF, OBJ_EVENT_GFX_MAY_SURFING)
K(GFX_THEO_RELIC, OBJ_EVENT_GFX_BRENDAN_FIELD_MOVE)
K(GFX_IANTHE_RELIC, OBJ_EVENT_GFX_MAY_FIELD_MOVE)
K(ANIM_SURF_TRANSITION, ANIM_GET_ON_OFF_POKEMON_SOUTH)
K(EFFECT_TALL, FLDEFF_TALL_GRASS)
K(EFFECT_LONG, FLDEFF_LONG_GRASS)
K(EFFECT_JUMP_TALL, FLDEFF_JUMP_TALL_GRASS)
K(EFFECT_JUMP_LONG, FLDEFF_JUMP_LONG_GRASS)
K(EFFECT_SAND, FLDEFF_SAND_FOOTPRINTS)
K(EFFECT_EXCLAMATION, FLDEFF_EXCLAMATION_MARK_ICON)
K(EFFECT_QUESTION, FLDEFF_QUESTION_MARK_ICON)
K(EFFECT_DOUBLE, FLDEFF_DOUBLE_EXCL_MARK_ICON)
K(EFFECT_X, FLDEFF_X_ICON)
K(EFFECT_HEART, FLDEFF_HEART_ICON)
K(EFFECT_SHADOW, FLDEFF_SHADOW)
K(TRAINER_FLAGS_END, TRAINER_FLAGS_END)
K(PAL_THEO, OBJ_EVENT_PAL_TAG_BRENDAN)
K(PAL_IANTHE, OBJ_EVENT_PAL_TAG_MAY)
K(PAL_SHADOW, TAG_WEATHER_START)

// These helpers are assembled into the test-only EWRAM blob, never the ROM.
bool8 ElaiaEffects_Start(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    bool8 used[MAX_SPRITES];
    u32 i;
    gSpecialVar_0x8005 = MAX_SPRITES;
    if (gSpecialVar_0x8000 == FLDEFF_EMOTE && (s16)gSpecialVar_0x8001 >= 0)
    {
        owner = GetFollowerObject();
        if (owner == NULL || !owner->active || !IsFollowerVisible())
            return FALSE;
    }
    for (i = 0; i < MAX_SPRITES; i++)
        used[i] = gSprites[i].inUse;
    for (i = 0; i < 8; i++)
        gFieldEffectArguments[i] = 0;
    gFieldEffectArguments[0] = owner->localId;
    gFieldEffectArguments[1] = owner->mapNum;
    gFieldEffectArguments[2] = owner->mapGroup;
    gFieldEffectArguments[7] = (s16)gSpecialVar_0x8001;
    if (gSpecialVar_0x8000 == FLDEFF_TALL_GRASS
     || gSpecialVar_0x8000 == FLDEFF_LONG_GRASS
     || gSpecialVar_0x8000 == FLDEFF_JUMP_TALL_GRASS
     || gSpecialVar_0x8000 == FLDEFF_JUMP_LONG_GRASS
     || gSpecialVar_0x8000 == FLDEFF_SAND_FOOTPRINTS)
    {
        gFieldEffectArguments[0] = owner->currentCoords.x;
        gFieldEffectArguments[1] = owner->currentCoords.y;
        gFieldEffectArguments[2] = 3;
        gFieldEffectArguments[3] = 1;
        gFieldEffectArguments[4] = (owner->localId << 8) | owner->mapNum;
        gFieldEffectArguments[5] = owner->mapGroup;
        gFieldEffectArguments[6] = (owner->mapNum << 8) | owner->mapGroup;
        gFieldEffectArguments[7] = 0;
        if (gSpecialVar_0x8000 == FLDEFF_SAND_FOOTPRINTS)
            gFieldEffectArguments[4] = gSpecialVar_0x8001;
    }
    FieldEffectStart(gSpecialVar_0x8000);
    gSpecialVar_0x8005 = MAX_SPRITES;
    for (i = 0; i < MAX_SPRITES; i++)
        if (!used[i] && gSprites[i].inUse)
            gSpecialVar_0x8005 = i;
    return FALSE;
}

bool8 ElaiaEffects_Follower(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = GetFollowerObject();
    gSpecialVar_0x8005 = owner != NULL && owner->active && IsFollowerVisible()
                      ? owner->spriteId : MAX_SPRITES;
    return FALSE;
}

bool8 ElaiaEffects_Arrow(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    gSpecialVar_0x8005 = CreateWarpArrowSprite();
    if (gSpecialVar_0x8005 < MAX_SPRITES)
        ShowWarpArrowSprite(gSpecialVar_0x8005, gSpecialVar_0x8001,
                            owner->currentCoords.x + 1, owner->currentCoords.y);
    return FALSE;
}

bool8 ElaiaEffects_Shadow(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    struct Sprite *sprite;
    gSpecialVar_0x8005 = CreateSpriteAtEndUnchecked(
        gFieldEffectObjectTemplatePointers[FLDEFFOBJ_SHADOW_S + gSpecialVar_0x8001],
        0, 0, 0x53);
    if (gSpecialVar_0x8005 < MAX_SPRITES)
    {
        sprite = &gSprites[gSpecialVar_0x8005];
        sprite->oam.objMode = ST_OAM_OBJ_BLEND;
        sprite->coordOffsetEnabled = TRUE;
        sprite->data[0] = owner->localId;
        sprite->data[1] = owner->mapNum;
        sprite->data[2] = owner->mapGroup;
        sprite->data[3] = gSpecialVar_0x8001 == 3 ? 16 : 4;
        gSpecialVar_0x8007 = GetSpritePaletteTagByPaletteNum(sprite->oam.paletteNum);
    }
    return FALSE;
}

bool8 ElaiaEffects_Terrain(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 x = owner->currentCoords.x;
    s16 y = owner->currentCoords.y;
    gSpecialVar_0x8007 = gBackupMapLayout.map[y * gBackupMapLayout.width + x];
    gBackupMapLayout.map[y * gBackupMapLayout.width + x] = gSpecialVar_0x8000;
    DrawWholeMapView();
    return FALSE;
}

bool8 ElaiaEffects_State(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    u8 id;
    RemoveObjectEventByLocalIdAndMap(0x50, owner->mapNum, owner->mapGroup);
    id = SpawnSpecialObjectEventParameterized(gSpecialVar_0x8000,
             MOVEMENT_TYPE_FACE_DOWN, 0x50, owner->currentCoords.x - 2,
             owner->currentCoords.y, 3);
    gSpecialVar_0x8005 = MAX_SPRITES;
    if (id < OBJECT_EVENTS_COUNT)
    {
        struct Sprite *sprite = &gSprites[gObjectEvents[id].spriteId];
        // Exercise the real state table without an NPC movement callback
        // replacing it. This is not proof of early-game controller eligibility.
        sprite->callback = SpriteCallbackDummy;
        sprite->animPaused = FALSE;
        StartSpriteAnim(sprite, gSpecialVar_0x8001);
        gSpecialVar_0x8005 = gObjectEvents[id].spriteId;
        gSpecialVar_0x8006 = id;
        gSpecialVar_0x8007 = GetSpritePaletteTagByPaletteNum(sprite->oam.paletteNum);
    }
    return FALSE;
}

bool8 ElaiaEffects_Inspect(struct ScriptContext *ctx)
{
    if (gSpecialVar_0x8005 < MAX_SPRITES)
        gSpecialVar_0x800A = gSprites[gSpecialVar_0x8005].animEnded;
    return FALSE;
}

bool8 ElaiaEffects_Free(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (gSpecialVar_0x8002 == 2)
        RemoveObjectEventByLocalIdAndMap(OBJ_EVENT_ID_FOLLOWER, owner->mapNum, owner->mapGroup);
    else if (gSpecialVar_0x8002 == 1)
    {
        RemoveObjectEventByLocalIdAndMap(0x50, owner->mapNum, owner->mapGroup);
        LoadPlayerObjectEventPalette(gSaveBlock2Ptr->playerGender);
    }
    else if (gSpecialVar_0x8005 < MAX_SPRITES
          && gSprites[gSpecialVar_0x8005].inUse)
        FieldEffectStop(&gSprites[gSpecialVar_0x8005], gSpecialVar_0x8000);
    return FALSE;
}
