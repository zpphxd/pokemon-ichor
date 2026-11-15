// Ichor: Arkadia's scenes that need the engine (design/phase3/SCRIPT.md, beats 42-43,
// STORY.md §6.4): a figure fading in and out at the Cypress Wood's tree line through
// a 16-frame blend, and Iapetos's wax tablet in a picture window. Every function
// here is a special (data/specials.inc); the scripts are
// data/maps/Arkadia_CypressWood/scripts.pory. See include/ichor_arkadia.h.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "gpu_regs.h"
#include "ichor_arkadia.h"
#include "menu.h"
#include "script_menu.h"
#include "sprite.h"
#include "task.h"

// --------------------------------------------------------------------------
// The blend: one object turns semi-transparent and its weight eases from 0 to
// 16 (fading in) or back (fading out) over 16 frames. The blend registers are
// put back as they were when it's done. The script waits with delay(18).
// --------------------------------------------------------------------------

#define BLEND_FRAMES 16

#define tSpriteId  data[0]
#define tFrame     data[1]
#define tFadeIn    data[2]
#define tOldCnt    data[3]
#define tOldAlpha  data[4]

static void Task_ObjectBlend(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    struct Sprite *sprite = &gSprites[tSpriteId];
    u32 weight;

    tFrame++;
    weight = tFadeIn ? tFrame : BLEND_FRAMES - tFrame;
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(weight, BLEND_FRAMES - weight));
    if (tFrame >= BLEND_FRAMES)
    {
        if (tFadeIn)
            sprite->oam.objMode = ST_OAM_OBJ_NORMAL;
        else
            sprite->invisible = TRUE;
        SetGpuReg(REG_OFFSET_BLDCNT, tOldCnt);
        SetGpuReg(REG_OFFSET_BLDALPHA, tOldAlpha);
        DestroyTask(taskId);
    }
}

static void StartObjectBlend(bool32 fadeIn)
{
    u8 objectEventId;
    u8 taskId;
    struct Sprite *sprite;

    if (TryGetObjectEventIdByLocalIdAndMap(gSpecialVar_0x8004, gSaveBlock1Ptr->location.mapNum,
                                           gSaveBlock1Ptr->location.mapGroup, &objectEventId))
        return;
    sprite = &gSprites[gObjectEvents[objectEventId].spriteId];
    taskId = CreateTask(Task_ObjectBlend, 80);
    gTasks[taskId].tSpriteId = gObjectEvents[objectEventId].spriteId;
    gTasks[taskId].tFrame = 0;
    gTasks[taskId].tFadeIn = fadeIn;
    gTasks[taskId].tOldCnt = GetGpuReg(REG_OFFSET_BLDCNT);
    gTasks[taskId].tOldAlpha = GetGpuReg(REG_OFFSET_BLDALPHA);
    sprite->oam.objMode = ST_OAM_OBJ_BLEND;
    sprite->invisible = FALSE;
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG_ALL | BLDCNT_TGT2_BD | BLDCNT_EFFECT_BLEND);
    SetGpuReg(REG_OFFSET_BLDALPHA, fadeIn ? BLDALPHA_BLEND(0, BLEND_FRAMES) : BLDALPHA_BLEND(BLEND_FRAMES, 0));
}

// The object with local id gSpecialVar_0x8004 (already added) fades in.
void Ichor_ObjectFadeIn(void)
{
    StartObjectBlend(TRUE);
}

// It fades out; remove it afterwards (removeobject sets its hide flag).
void Ichor_ObjectFadeOut(void)
{
    StartObjectBlend(FALSE);
}

#undef tSpriteId
#undef tFrame
#undef tFadeIn
#undef tOldCnt
#undef tOldAlpha

// --------------------------------------------------------------------------
// Iapetos's wax tablet: fresh wax, a neat hand, a little hook at the end of the
// last line (beat 42). A picture window like Alethea's program (beat 32).
// --------------------------------------------------------------------------

#define TAG_TABLET 0x4A33

static const u32 sTabletGfx[] = INCBIN_U32("graphics/ichor/act2/kleon_tablet.4bpp");
static const u16 sTabletPal[] = INCBIN_U16("graphics/ichor/act2/kleon_tablet.gbapal");

static const struct OamData sOam_Tablet =
{
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct SpriteTemplate sSpriteTemplate_Tablet =
{
    .tileTag = TAG_TABLET,
    .paletteTag = TAG_TABLET,
    .oam = &sOam_Tablet,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

#define TABLET_X 10   // the box's tile position, as ScriptMenu_ShowPokemonPic takes it
#define TABLET_Y 2

static EWRAM_DATA u8 sTabletWindowId = 0;
static EWRAM_DATA u8 sTabletSpriteId = 0;
static EWRAM_DATA bool8 sTabletShown = FALSE;

void Ichor_ShowKleonTablet(void)
{
    struct SpriteSheet sheet = {sTabletGfx, sizeof(sTabletGfx), TAG_TABLET};
    struct SpritePalette pal = {sTabletPal, TAG_TABLET};

    if (sTabletShown)
        return;
    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&pal);
    sTabletSpriteId = CreateSprite(&sSpriteTemplate_Tablet, TABLET_X * 8 + 40, TABLET_Y * 8 + 40, 0);
    sTabletWindowId = CreateWindowFromRect(TABLET_X, TABLET_Y, 8, 8);
    SetStandardWindowBorderStyle(sTabletWindowId, TRUE);
    ScheduleBgCopyTilemapToVram(0);
    sTabletShown = TRUE;
}

void Ichor_HideKleonTablet(void)
{
    if (!sTabletShown)
        return;
    DestroySprite(&gSprites[sTabletSpriteId]);
    FreeSpriteTilesByTag(TAG_TABLET);
    FreeSpritePaletteByTag(TAG_TABLET);
    ClearToTransparentAndRemoveWindow(sTabletWindowId);
    sTabletShown = FALSE;
}
