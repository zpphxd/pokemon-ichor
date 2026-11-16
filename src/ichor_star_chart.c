#include "global.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "ichor_star_chart.h"
#include "item_menu.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

struct Constellation
{
    const u8 *name;
    u8 count;
    u8 points[7][2];
};

static const struct Constellation sStars[ICHOR_STAR_COUNT] =
{
    {COMPOUND_STRING("Delphinus"), 6, {{2,16},{10,8},{17,2},{25,8},{17,13},{10,8}}},
    {COMPOUND_STRING("Crater"), 6, {{2,2},{7,11},{21,11},{26,2},{14,11},{14,18}}},
    {COMPOUND_STRING("Ursa Major"), 7, {{1,4},{8,6},{13,9},{18,8},{26,11},{23,17},{15,14}}},
    {COMPOUND_STRING("Orion"), 7, {{5,2},{11,8},{17,8},{24,2},{17,8},{17,17},{6,17}}},
    {COMPOUND_STRING("Sagitta"), 5, {{2,14},{24,3},{17,3},{24,3},{21,10}}},
    {COMPOUND_STRING("Cygnus"), 6, {{14,1},{14,18},{14,8},{2,6},{14,8},{27,6}}},
    {COMPOUND_STRING("Taurus"), 7, {{1,1},{8,9},{15,6},{26,1},{15,6},{22,16},{8,9}}},
    {COMPOUND_STRING("Corona Borealis"), 6, {{2,3},{5,12},{11,17},{19,17},{25,11},{27,2}}},
    {COMPOUND_STRING("Pleiades"), 7, {{7,5},{13,2},{19,6},{23,12},{16,16},{9,12},{14,9}}},
    {COMPOUND_STRING("Corvus"), 5, {{7,2},{22,4},{25,15},{3,17},{7,2}}},
    {COMPOUND_STRING("Lyra"), 6, {{4,1},{9,8},{24,7},{20,17},{6,17},{9,8}}},
    {COMPOUND_STRING("Capricornus"), 6, {{2,2},{13,6},{27,1},{22,13},{10,18},{2,2}}},
    {COMPOUND_STRING("Cancer"), 7, {{2,3},{14,9},{25,2},{14,9},{14,17},{5,14},{14,9}}},
    {COMPOUND_STRING("Aries"), 4, {{3,14},{10,7},{21,5},{26,10}}},
    {COMPOUND_STRING("Gemini"), 7, {{6,1},{8,9},{4,18},{8,9},{22,8},{21,1},{22,18}}},
    {COMPOUND_STRING("Aquila"), 7, {{1,11},{11,6},{14,1},{17,6},{28,11},{17,6},{14,18}}},
    {COMPOUND_STRING("Ophiuchus"), 7, {{14,1},{5,8},{8,17},{20,17},{24,8},{14,1},{14,12}}},
    {COMPOUND_STRING("Leo"), 7, {{5,3},{12,1},{16,6},{11,10},{27,16},{6,17},{11,10}}},
    {COMPOUND_STRING("Hydra"), 7, {{1,3},{5,7},{10,4},{14,10},{19,8},{23,16},{28,14}}},
    {COMPOUND_STRING("Draco"), 7, {{2,15},{8,10},{4,4},{13,1},{23,5},{26,13},{19,16}}},
    {COMPOUND_STRING("Hercules"), 7, {{2,3},{9,8},{12,2},{18,9},{27,4},{18,9},{14,18}}},
    {COMPOUND_STRING("Centaurus"), 7, {{2,17},{6,10},{19,10},{26,17},{19,10},{20,2},{28,5}}},
    {COMPOUND_STRING("Cetus"), 7, {{2,9},{7,2},{22,3},{27,10},{19,17},{6,15},{2,9}}},
    {COMPOUND_STRING("The Unwoven"), 7, {{14,1},{14,8},{3,5},{14,8},{25,5},{14,8},{9,18}}},
};

bool32 Ichor_PlaceStar(u32 star)
{
    if (star >= ICHOR_STAR_COUNT || FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + star))
        return FALSE;
    FlagSet(FLAG_ICHOR_CONSTELLATIONS_START + star);
    return TRUE;
}

u32 Ichor_CountStars(void)
{
    return Ichor_CountFlags(FLAG_ICHOR_CONSTELLATIONS_START, ICHOR_STAR_COUNT);
}

u16 Ichor_PlaceConstellation(void)
{
    return Ichor_PlaceStar(gSpecialVar_0x8004);
}

u16 Ichor_CountConstellations(void)
{
    return Ichor_CountStars();
}

void Ichor_StarFlagSet(u16 flag)
{
    switch (flag)
    {
    case FLAG_ICHOR_GOT_POSEIDONS_CONCH: Ichor_PlaceStar(ICHOR_STAR_DELPHINUS); break;
    case FLAG_BADGE04_GET: Ichor_PlaceStar(ICHOR_STAR_CRATER); break;
    case FLAG_BADGE05_GET: Ichor_PlaceStar(ICHOR_STAR_URSA_MAJOR); break;
    case FLAG_BADGE07_GET: Ichor_PlaceStar(ICHOR_STAR_CYGNUS); break;
    case FLAG_BADGE08_GET: Ichor_PlaceStar(ICHOR_STAR_CORVUS); break;
    }
}

void Ichor_RefreshStars(void)
{
    static const u16 receipts[] =
    {
        FLAG_ICHOR_GOT_POSEIDONS_CONCH, FLAG_BADGE04_GET, FLAG_BADGE05_GET,
        FLAG_BADGE07_GET, FLAG_BADGE08_GET,
    };
    u32 i;
    for (i = 0; i < ARRAY_COUNT(receipts); i++)
        if (FlagGet(receipts[i]))
            Ichor_StarFlagSet(receipts[i]);
    if (Ichor_GetFavor(ICHOR_GOD_ARTEMIS) >= 30)
        Ichor_PlaceStar(ICHOR_STAR_ORION);
    if (Ichor_GetFavor(ICHOR_GOD_HERA) >= 30)
        Ichor_PlaceStar(ICHOR_STAR_CANCER);
    if (Ichor_CountFlags(FLAG_ICHOR_PAGES_START, 7) == 7)
        Ichor_PlaceStar(ICHOR_STAR_PLEIADES);
}

struct StarChart
{
    u16 tilemaps[3][1024];
    u8 selected;
    u8 pulse;
    bool8 closing;
};

static EWRAM_DATA struct StarChart *sStarChart = NULL;
enum { WIN_SKY, WIN_STARS, WIN_HEADER, WIN_FOOTER };

static const struct BgTemplate sBgs[] =
{
    {.bg = 0, .charBaseIndex = 3, .mapBaseIndex = 30, .priority = 0},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 29, .priority = 1},
    {.bg = 2, .charBaseIndex = 0, .mapBaseIndex = 28, .priority = 2},
};
static const struct WindowTemplate sWindows[] =
{
    {.bg = 2, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 20, .paletteNum = 13, .baseBlock = 1},
    {.bg = 1, .tilemapLeft = 0, .tilemapTop = 2, .width = 30, .height = 16, .paletteNum = 14, .baseBlock = 1},
    {.bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 2, .paletteNum = 15, .baseBlock = 1},
    {.bg = 0, .tilemapLeft = 0, .tilemapTop = 17, .width = 30, .height = 3, .paletteNum = 15, .baseBlock = 61},
    DUMMY_WIN_TEMPLATE,
};
static const u16 sPalettes[3][16] =
{
    {RGB(29,25,18), RGB(29,25,18), RGB(14,7,3), RGB(26,20,12)},
    {RGB(0,0,0), RGB(14,7,3), RGB(30,19,4), RGB(20,13,7)},
    {RGB(0,0,0), RGB(29,25,18), RGB(14,7,3), RGB(26,20,12)},
};

extern const u8 EventScript_IchorChartError[];

static void FieldCB_ChartError(void)
{
    ScriptContext_SetupScript(EventScript_IchorChartError);
}

static void ReleaseChart(void)
{
    SetVBlankCallback(NULL);
    FreeAllWindowBuffers();
    Free(sStarChart);
    sStarChart = NULL;
}

static void VBlank_StarChart(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void DrawLine(s32 x, s32 y, s32 targetX, s32 targetY)
{
    s32 dx = abs(targetX - x), dy = -abs(targetY - y);
    s32 stepX = x < targetX ? 1 : -1;
    s32 stepY = y < targetY ? 1 : -1;
    s32 error = dx + dy;
    while (TRUE)
    {
        s32 twice;
        FillWindowPixelRect(WIN_STARS, PIXEL_FILL(1), x, y, 1, 1);
        if (x == targetX && y == targetY)
            break;
        twice = 2 * error;
        if (twice >= dy) { error += dy; x += stepX; }
        if (twice <= dx) { error += dx; y += stepY; }
    }
}

static void DrawChart(void)
{
    static const u8 colors[] = {0, 2, 3};
    u32 star, point;
    u8 text[64], *end;
    FillWindowPixelBuffer(WIN_STARS, PIXEL_FILL(0));
    for (star = 0; star < ICHOR_STAR_COUNT; star++)
    {
        u32 x = 8 + (star % 6) * 38, y = 6 + (star / 6) * 28;
        const struct Constellation *shape = &sStars[star];
        if (FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + star))
        {
            for (point = 1; point < shape->count; point++)
                DrawLine(x + shape->points[point - 1][0], y + shape->points[point - 1][1],
                         x + shape->points[point][0], y + shape->points[point][1]);
            for (point = 0; point < shape->count; point++)
                FillWindowPixelRect(WIN_STARS, PIXEL_FILL(2), x + shape->points[point][0] - 1, y + shape->points[point][1] - 1, 3, 3);
        }
        if (star == sStarChart->selected)
        {
            FillWindowPixelRect(WIN_STARS, PIXEL_FILL(3), x - 2, y - 2, 33, 1);
            FillWindowPixelRect(WIN_STARS, PIXEL_FILL(3), x - 2, y + 20, 33, 1);
            FillWindowPixelRect(WIN_STARS, PIXEL_FILL(3), x - 2, y - 2, 1, 23);
            FillWindowPixelRect(WIN_STARS, PIXEL_FILL(3), x + 30, y - 2, 1, 23);
        }
    }
    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(0));
    end = StringCopy(text, COMPOUND_STRING("STAR CHART   "));
    end = ConvertIntToDecimalStringN(end, Ichor_CountStars(), STR_CONV_MODE_LEFT_ALIGN, 2);
    StringCopy(end, COMPOUND_STRING("/24"));
    AddTextPrinterParameterized4(WIN_HEADER, FONT_SMALL, 8, 1, 0, 0, colors, TEXT_SKIP_DRAW, text);
    FillWindowPixelBuffer(WIN_FOOTER, PIXEL_FILL(0));
    StringCopy(text, FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + sStarChart->selected)
                    ? sStars[sStarChart->selected].name : COMPOUND_STRING("An empty patch of sky."));
    AddTextPrinterParameterized4(WIN_FOOTER, FONT_SMALL, 8, 0, 0, 0, colors, TEXT_SKIP_DRAW, text);
    AddTextPrinterParameterized4(WIN_FOOTER, FONT_SMALL, 8, 12, 0, 0, colors, TEXT_SKIP_DRAW, COMPOUND_STRING("D-pad: patches   B: Bag"));
    CopyWindowToVram(WIN_STARS, COPYWIN_FULL);
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
    CopyWindowToVram(WIN_FOOTER, COPYWIN_FULL);
}

static void Task_StarChart(u8 taskId)
{
    u32 selected;
    if (gPaletteFade.active)
        return;
    if (sStarChart->closing)
    {
        ReleaseChart();
        DestroyTask(taskId);
        SetMainCallback2(CB2_ReturnToBagMenuPocket);
        return;
    }
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sStarChart->closing = TRUE;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        return;
    }
    selected = sStarChart->selected;
    if (JOY_NEW(DPAD_RIGHT)) selected = (selected + 1) % ICHOR_STAR_COUNT;
    else if (JOY_NEW(DPAD_LEFT)) selected = (selected + ICHOR_STAR_COUNT - 1) % ICHOR_STAR_COUNT;
    else if (JOY_NEW(DPAD_DOWN)) selected = (selected + 6) % ICHOR_STAR_COUNT;
    else if (JOY_NEW(DPAD_UP)) selected = (selected + ICHOR_STAR_COUNT - 6) % ICHOR_STAR_COUNT;
    if (selected != sStarChart->selected)
    {
        sStarChart->selected = selected;
        PlaySE(SE_SELECT);
        DrawChart();
    }
    sStarChart->pulse = (sStarChart->pulse + 1) % 24;
    if (sStarChart->pulse % 12 == 0)
    {
        u16 color = sStarChart->pulse % 24 == 0 ? RGB(30,19,4) : RGB(31,28,15);
        LoadPalette(&color, BG_PLTT_ID(14) + 2, sizeof(color));
    }
}

static void CB2_StarChart(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void CB2_InitStarChart(void)
{
    u32 bg;
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    ScanlineEffect_Stop();
    DmaFill16(3, 0, VRAM, VRAM_SIZE);
    DmaFill32(3, 0, OAM, OAM_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgs, ARRAY_COUNT(sBgs));
    for (bg = 0; bg < 3; bg++)
    {
        SetBgTilemapBuffer(bg, sStarChart->tilemaps[bg]);
        ChangeBgX(bg, 0, BG_COORD_SET);
        ChangeBgY(bg, 0, BG_COORD_SET);
    }
    if (!InitWindows(sWindows))
    {
        ReleaseChart();
        gFieldCallback = FieldCB_ChartError;
        SetMainCallback2(CB2_ReturnToField);
        return;
    }
    DeactivateAllTextPrinters();
    LoadPalette(sPalettes, BG_PLTT_ID(13), sizeof(sPalettes));
    FillWindowPixelBuffer(WIN_SKY, PIXEL_FILL(1));
    FillWindowPixelRect(WIN_SKY, PIXEL_FILL(2), 2, 17, 236, 1);
    FillWindowPixelRect(WIN_SKY, PIXEL_FILL(2), 2, 134, 236, 1);
    FillWindowPixelRect(WIN_SKY, PIXEL_FILL(2), 2, 17, 1, 118);
    FillWindowPixelRect(WIN_SKY, PIXEL_FILL(2), 237, 17, 1, 118);
    PutWindowTilemap(WIN_SKY);
    PutWindowTilemap(WIN_STARS);
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_FOOTER);
    CopyWindowToVram(WIN_SKY, COPYWIN_FULL);
    DrawChart();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ShowBg(2);
    ShowBg(1);
    ShowBg(0);
    BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlank_StarChart);
    SetMainCallback2(CB2_StarChart);
    CreateTask(Task_StarChart, 0);
}

void ItemUseOutOfBattle_IchorStarChart(u8 taskId)
{
    if (ItemUse_IchorIsFromField(taskId))
    {
        ItemUse_IchorMessage(taskId, COMPOUND_STRING("Open the Star Chart from your Bag."));
        return;
    }
    sStarChart = AllocZeroed(sizeof(*sStarChart));
    if (sStarChart == NULL)
    {
        ItemUse_IchorMessage(taskId, COMPOUND_STRING("The chart cannot be opened.\nTry again after saving."));
        return;
    }
    Ichor_RefreshStars();
    ItemUse_IchorOpenScreenFromBag(taskId, CB2_InitStarChart);
}
