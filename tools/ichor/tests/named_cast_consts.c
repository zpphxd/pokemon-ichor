#include "engine_consts.h"
#include "sprite.h"
#include "script.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "trainer_pokemon_sprites.h"
#include "palette.h"
#include "data.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/trainers.h"

#define G(name) K(GFX_##name, OBJ_EVENT_GFX_ICHOR_##name)
G(AIAKIDES)
G(ALETHEA)
G(APOLLO)
G(CAMI)
G(DEMETER)
G(ENDEIS)
G(KEDALION)
G(KERYKOS)
G(KLEON)
G(KLEON_SEASICK)
G(KLEON_TABLET)
G(MOM)
G(PHEIDON)
G(PROFESSOR_DAPHNE)
G(PRONOMOS)
G(SAM)
G(HIEROPHANT_IONE)
G(TITAN_GRUNT)
#define T(name) K(PIC_##name, TRAINER_PIC_##name)
T(ALETHEA)
T(HIEROPHANT_IONE)
T(HIEROPHANT_KERYKOS)
T(KLEON)
T(PROFESSOR_DAPHNE)
T(TITAN_GRUNT)
K(SPRITE_SIZE, sizeof(struct Sprite))
K(SPRITE_LIMIT, MAX_SPRITES)
K(OFF_SPRITE_IMAGES, offsetof(struct Sprite, images))
K(FRAME_IMAGE_SIZE, sizeof(struct SpriteFrameImage))
K(OFF_FRAME_IMAGE_DATA, offsetof(struct SpriteFrameImage, data))
K(OFF_FRAME_IMAGE_SIZE, offsetof(struct SpriteFrameImage, size))
K(OFF_FRAME_IMAGE_RELATIVE, offsetof(struct SpriteFrameImage, relativeFrames))
K(PAL_CAST, OBJ_EVENT_PAL_TAG_ICHOR_CAST)
K(PAL_FOLK, OBJ_EVENT_PAL_TAG_ICHOR_FOLK)
K(PAL_THEOXENIA, OBJ_EVENT_PAL_TAG_ICHOR_THEOXENIA)
K(TRAINER_INFO_SIZE, sizeof(struct TrainerPicInfo))
K(OFF_TRAINER_FRONT, offsetof(struct TrainerPicInfo, frontPic))
K(OFF_TRAINER_BACK, offsetof(struct TrainerPicInfo, backPic))
K(OFF_FRONT_PALETTE, offsetof(struct TrainerFrontPicInfo, paletteData))
K(OFF_BACK_PALETTE, offsetof(struct TrainerBackPicInfo, paletteData))
K(VAR_0x8003, VAR_0x8003)
K(VAR_0x800A, VAR_0x800A)

bool8 NamedCast_Open(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    u8 id;
    gSpecialVar_0x8005 = MAX_SPRITES;
    if (gSpecialVar_0x8001 == 0)
    {
        id = SpawnSpecialObjectEventParameterized(gSpecialVar_0x8000,
                 MOVEMENT_TYPE_FACE_DOWN, 0x50, owner->currentCoords.x - 2,
                 owner->currentCoords.y, 3);
        if (id < OBJECT_EVENTS_COUNT)
            gSpecialVar_0x8005 = gObjectEvents[id].spriteId;
    }
    else
    {
        gSpecialVar_0x8005 = CreateTrainerPicSprite(gSpecialVar_0x8000,
                                gSpecialVar_0x8001 == 1, 120, 60, 14, TAG_NONE);
        if (gSpecialVar_0x8001 == 2)
            LoadPalette(GetTrainerBackPicPalette(gSpecialVar_0x8000),
                        OBJ_PLTT_ID(14), PLTT_SIZE_4BPP);
    }
    if (gSpecialVar_0x8005 < MAX_SPRITES)
    {
        struct Sprite *sprite = &gSprites[gSpecialVar_0x8005];
        sprite->callback = SpriteCallbackDummy;
        sprite->animPaused = TRUE;
        sprite->animBeginning = FALSE;
        sprite->animDelayCounter = 0;
        gSpecialVar_0x800A = GetSpritePaletteTagByPaletteNum(sprite->oam.paletteNum);
    }
    return FALSE;
}

bool8 NamedCast_Frame(struct ScriptContext *ctx)
{
    struct Sprite *sprite = &gSprites[gSpecialVar_0x8005];
    const struct SpriteFrameImage *image = &sprite->images[
        sprite->images[0].relativeFrames ? 0 : gSpecialVar_0x8002];
    sprite->animPaused = TRUE;
    sprite->hFlip = gSpecialVar_0x8003;
    sprite->oam.matrixNum = (sprite->oam.matrixNum & 7) | (gSpecialVar_0x8003 ? 8 : 0);
    gSpecialVar_0x8007 = image->size;
    RequestSpriteFrameImageCopy(gSpecialVar_0x8002, sprite->oam.tileNum, sprite->images);
    return FALSE;
}

bool8 NamedCast_Free(struct ScriptContext *ctx)
{
    struct ObjectEvent *owner = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (gSpecialVar_0x8001 == 0)
        RemoveObjectEventByLocalIdAndMap(0x50, owner->mapNum, owner->mapGroup);
    else if (gSpecialVar_0x8005 < MAX_SPRITES)
        FreeAndDestroyTrainerPicSprite(gSpecialVar_0x8005);
    return FALSE;
}
