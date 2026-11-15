#include "elaia_effects_consts.c"

K(GFX_THEO_UNDERWATER, OBJ_EVENT_GFX_BRENDAN_UNDERWATER)
K(GFX_IANTHE_UNDERWATER, OBJ_EVENT_GFX_MAY_UNDERWATER)
K(PAL_UNDERWATER, OBJ_EVENT_PAL_TAG_PLAYER_UNDERWATER)
K(OFF_SPRITE_X, offsetof(struct Sprite, x))
K(OFF_SPRITE_Y, offsetof(struct Sprite, y))
K(OFF_SPRITE_Y2, offsetof(struct Sprite, y2))

bool8 ElaiaWater_State(struct ScriptContext *ctx)
{
    gSaveBlock2Ptr->playerGender = gSpecialVar_0x8003;
    ElaiaEffects_State(ctx);
    gSpecialVar_0x800B = MAX_SPRITES;
    if (gSpecialVar_0x8005 < MAX_SPRITES)
    {
        struct ObjectEvent *object = &gObjectEvents[gSpecialVar_0x8006];
        struct Sprite *rider = &gSprites[object->spriteId];
        object->movementDirection = gSpecialVar_0x8004;
        object->facingDirection = gSpecialVar_0x8004;
        if (gSpecialVar_0x8000 == OBJ_EVENT_GFX_BRENDAN_SURFING
         || gSpecialVar_0x8000 == OBJ_EVENT_GFX_MAY_SURFING)
        {
            gFieldEffectArguments[0] = object->currentCoords.x;
            gFieldEffectArguments[1] = object->currentCoords.y;
            gFieldEffectArguments[2] = gSpecialVar_0x8006;
            gSpecialVar_0x800B = FieldEffectStart(FLDEFF_SURF_BLOB);
            if (gSpecialVar_0x800B < MAX_SPRITES)
            {
                SetSurfBlob_BobState(gSpecialVar_0x800B, BOB_PLAYER_AND_MON);
                gSpecialVar_0x800A = GetSpritePaletteTagByPaletteNum(
                    gSprites[gSpecialVar_0x800B].oam.paletteNum);
            }
        }
        else
        {
            // The existing underwater state uses a hidden native bob helper,
            // not the surface dolphin; retain that exact renderer behavior.
            gSpecialVar_0x800B = StartUnderwaterSurfBlobBobbing(object->spriteId);
            rider->y2 = 0;
        }
    }
    return FALSE;
}

bool8 ElaiaWater_Free(struct ScriptContext *ctx)
{
    if (gSpecialVar_0x800B < MAX_SPRITES && gSprites[gSpecialVar_0x800B].inUse)
        DestroySprite(&gSprites[gSpecialVar_0x800B]);
    gSpecialVar_0x8002 = 1;
    return ElaiaEffects_Free(ctx);
}
