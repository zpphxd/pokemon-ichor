#include "global.h"
#include "bg.h"
#include "gpu_regs.h"
#include "ichor_oath.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "title_screen.h"
#include "window.h"
#include "constants/rgb.h"

static EWRAM_DATA u16 sOathEndTilemap[BG_SCREEN_SIZE / 2] = {0};

static const struct BgTemplate sBg =
{
    .bg = 0,
    .charBaseIndex = 0,
    .mapBaseIndex = 31,
};

static const struct WindowTemplate sWindows[] =
{
    {
        .bg = 0,
        .tilemapLeft = 1,
        .tilemapTop = 2,
        .width = 28,
        .height = 16,
        .paletteNum = 15,
        .baseBlock = 1,
    },
    DUMMY_WIN_TEMPLATE,
};

static void VBlank_OathEndScreen(void)
{
    LoadOam();
    TransferPlttBuffer();
}

static void CB2_OathEndScreen(void)
{
    UpdatePaletteFade();
    if (gPaletteFade.active)
        return;
    if (gMain.state == 0)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            gMain.state = 1;
        }
    }
    else
    {
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        UnsetBgTilemapBuffer(0);
        SetMainCallback2(CB2_InitTitleScreen);
    }
}

void Ichor_ShowOathEndScreen(bool32 capacityBlocked)
{
    const u8 *text = capacityBlocked
        ? COMPOUND_STRING("There is no room to recover\na living partner from storage.\n\nNo stored partners were moved.\nYour last manual save is unchanged.\n\nA/B: Return to title")
        : COMPOUND_STRING("Your Oath has ended.\nNo living partners remain.\n\nYour last manual save is unchanged.\n\nA/B: Return to title");

    SetMainCallback1(NULL);
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    StopMapMusic();
    ScanlineEffect_Stop();
    FreeAllWindowBuffers();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    DmaFill16(3, 0, VRAM, VRAM_SIZE);
    DmaFill32(3, 0, OAM, OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, &sBg, 1);
    CpuFill16(0, sOathEndTilemap, sizeof(sOathEndTilemap));
    SetBgTilemapBuffer(0, sOathEndTilemap);
    ChangeBgX(0, 0, BG_COORD_SET);
    ChangeBgY(0, 0, BG_COORD_SET);
    if (!InitWindows(sWindows))
    {
        DebugPrintfLevel(MGBA_LOG_ERROR, "Ichor: cannot allocate Oath ending screen");
        DoSoftReset();
        return;
    }
    DeactivateAllTextPrinters();
    LoadPalette(gStandardMenuPalette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    LoadUserWindowBorderGfx(0, 0x1D0, BG_PLTT_ID(14));
    DrawStdFrameWithCustomTileAndPalette(0, FALSE, 0x1D0, 14);
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    AddTextPrinterParameterized(0, FONT_NORMAL, text, 4, 4, TEXT_SKIP_DRAW, NULL);
    CopyWindowToVram(0, COPYWIN_FULL);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ShowBg(0);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlank_OathEndScreen);
    SetMainCallback2(CB2_OathEndScreen);
}
