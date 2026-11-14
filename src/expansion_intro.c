#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "palette.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "gpu_regs.h"
#include "trig.h"
#include "main.h"
#include "intro.h"
#include "intro_frlg.h"
#include "m4a.h"
#include "expansion_intro.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#if EXPANSION_INTRO == TRUE

// Ichor: the card is restyled as black gloss and gold (tools/ichor/art/intro_screen.py
// draws powered_by.png and rhh_credits.png). Upstream's walking egg and Porygon
// sprites, with their sounds, are left out of the pottery look.

enum
{
    EXPANSION_INTRO_BG2,
    EXPANSION_INTRO_BG3
};

static const u32 sBgTiles_PoweredBy[] = INCGFX_U32("graphics/expansion_intro/powered_by.png", ".4bpp.smol");
static const u32 sBgTiles_RhhCredits[] = INCGFX_U32("graphics/expansion_intro/rhh_credits.png", ".8bpp.smol");
static const u32 sBgMap_PoweredBy[] = INCGFX_U32("graphics/expansion_intro/powered_by.bin", ".smolTM");
static const u32 sBgMap_RhhCredits[] = INCGFX_U32("graphics/expansion_intro/rhh_credits.bin", ".smolTM");
static const u16 sBgPal_Credits[] = INCGFX_U16("graphics/expansion_intro/credits.pal", ".gbapal");

static void Task_ExpansionIntro_HandleBlend(u8 taskId);
static void VBlankCB_ExpansionIntro(void);
static void ExpansionIntro_InitBgs();
static void ExpansionIntro_StartBlend();
static void ExpansionIntro_LoadGraphics();

static const struct BgTemplate sBgTemplates_RhhCopyrightScreen[] =
{
    [EXPANSION_INTRO_BG2] = {
        .bg = 2,
        .charBaseIndex = 1,
        .mapBaseIndex = 20,
        .screenSize = 2,
        .paletteMode = 1
    },
    [EXPANSION_INTRO_BG3] = {
        .bg = 3,
        .mapBaseIndex = 22,
        .screenSize = 2
    },
};

void CB2_ExpansionIntro(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

#define tState gTasks[taskId].data[0]
#define tFrameCounter gTasks[taskId].data[1]
void Task_HandleExpansionIntro(u8 taskId)
{
    switch (tState)
    {
    case 0:
        SetVBlankCallback(VBlankCB_ExpansionIntro);
        ExpansionIntro_InitBgs();
        ExpansionIntro_LoadGraphics();
        CpuFastFill16(RGB_BLACK, gPlttBufferFaded, 32);
        ShowBg(3);
        BeginNormalPaletteFade(1, 0, 16, 0, RGB_BLACK);
        ExpansionIntro_StartBlend();
        tState++;
        break;
    case 1:
        if (!gPaletteFade.active)
            tState++;
        break;
    case 2:
        if (tFrameCounter == 208)
        {
            tState++;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        else if (gMain.newKeys != 0)
        {
            CpuFill16(0, gPlttBufferFaded, sizeof(gPlttBufferFaded));
            tState++;
        }
        else
        {
            tFrameCounter++;
        }
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            ResetSpriteData();
            FreeAllSpritePalettes();
            DestroyTask(taskId);
            if (IS_FRLG)
            {
                SetMainCallback2(CB2_SetUpIntroFrlg);
            }
            else
            {
                CreateTask(Task_Scene1_Load, 0);
                SetMainCallback2(MainCB2_Intro);
            }
        }
        break;
    }
}
#undef tState

static void VBlankCB_ExpansionIntro(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void ExpansionIntro_InitBgs(void)
{
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates_RhhCopyrightScreen, ARRAY_COUNT(sBgTemplates_RhhCopyrightScreen));
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_EFFECT_DARKEN);
    SetGpuReg(REG_OFFSET_BLDY, 0x1F);
    HideBg(0);
    HideBg(1);
    HideBg(2);
    HideBg(3);
}

static void ExpansionIntro_LoadGraphics(void)
{
    DecompressDataWithHeaderVram(sBgTiles_PoweredBy, (void*) BG_CHAR_ADDR(sBgTemplates_RhhCopyrightScreen[EXPANSION_INTRO_BG3].charBaseIndex));
    DecompressDataWithHeaderVram(sBgMap_PoweredBy, (u16*) BG_SCREEN_ADDR(sBgTemplates_RhhCopyrightScreen[EXPANSION_INTRO_BG3].mapBaseIndex));
    DecompressDataWithHeaderVram(sBgTiles_RhhCredits, (void*) BG_CHAR_ADDR(sBgTemplates_RhhCopyrightScreen[EXPANSION_INTRO_BG2].charBaseIndex));
    DecompressDataWithHeaderVram(sBgMap_RhhCredits, (u16*) BG_SCREEN_ADDR(sBgTemplates_RhhCopyrightScreen[EXPANSION_INTRO_BG2].mapBaseIndex));
    LoadPalette(sBgPal_Credits, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
}

static void ExpansionIntro_StartBlend(void)
{
    ShowBg(2);
    CreateTask(Task_ExpansionIntro_HandleBlend, 0);
}

static void Task_ExpansionIntro_HandleBlend(u8 taskId)
{
    if (GetGpuReg(REG_OFFSET_BLDY) != 0)
    {
        SetGpuReg(REG_OFFSET_BLDY, GetGpuReg(REG_OFFSET_BLDY) - 1);
    }
    else
    {
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        DestroyTask(taskId);
    }
}

#endif //EXPANSION_INTRO
