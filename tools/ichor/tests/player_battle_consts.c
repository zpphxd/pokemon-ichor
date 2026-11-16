#include "engine_consts.h"
#include "data.h"
#include "event_data.h"
#include "script.h"
#include "sprite.h"
#include "trainer_pokemon_sprites.h"

K(PIC_THEO, TRAINER_PIC_BRENDAN)
K(PIC_IANTHE, TRAINER_PIC_MAY)
K(SPRITE_SIZE, sizeof(struct Sprite))
K(SPRITE_LIMIT, MAX_SPRITES)
K(OFF_SPRITE_IMAGES, offsetof(struct Sprite, images))
K(OFF_SPRITE_ANIMS, offsetof(struct Sprite, anims))
K(OFF_SPRITE_ANIM_CMD, offsetof(struct Sprite, animCmdIndex))
K(FRAME_IMAGE_SIZE, sizeof(struct SpriteFrameImage))
K(PIC_BYTES, TRAINER_PIC_SIZE)
K(VAR_0x800A, VAR_0x800A)

bool8 PlayerBattle_Create(struct ScriptContext *ctx)
{
    u16 pic = gSpecialVar_0x8000;
    u16 id = CreateTrainerPicSprite(pic, gSpecialVar_0x8001, 120, 64, 14, TAG_NONE);
    gSpecialVar_0x8005 = id;
    if (id < MAX_SPRITES && !gSpecialVar_0x8001)
    {
        gSprites[id].anims = gTrainerPicInfo[pic].backPic->animation;
        StartSpriteAnim(&gSprites[id], gSpecialVar_0x8002);
        gSprites[id].animPaused = TRUE;
    }
    return FALSE;
}

bool8 PlayerBattle_Start(struct ScriptContext *ctx)
{
    if (gSpecialVar_0x8005 < MAX_SPRITES)
    {
        struct Sprite *sprite = &gSprites[gSpecialVar_0x8005];
        StartSpriteAnim(sprite, gSpecialVar_0x8002);
        sprite->animPaused = FALSE;
    }
    return FALSE;
}

bool8 PlayerBattle_Inspect(struct ScriptContext *ctx)
{
    gSpecialVar_0x800A = gSpecialVar_0x8005 < MAX_SPRITES
                     && gSprites[gSpecialVar_0x8005].animEnded;
    return FALSE;
}

bool8 PlayerBattle_Free(struct ScriptContext *ctx)
{
    if (gSpecialVar_0x8005 < MAX_SPRITES)
        FreeAndDestroyTrainerPicSprite(gSpecialVar_0x8005);
    return FALSE;
}
