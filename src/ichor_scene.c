// Ichor: small helpers for story scenes (design/phase2/SCRIPT.md).
// Scene support only; the Ichor systems (relics, rites, herms, save state)
// belong to the engine session and live in their own files.
#include "global.h"
#include "bg.h"
#include "event_data.h"
#include "ichor_scene.h"
#include "international_string_util.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "text.h"
#include "text_window.h"
#include "window.h"

static const u32 sTabletPicture[] = INCBIN_U32("graphics/ichor/tablet_back.4bpp");
static const u16 sTabletPalette[] = INCBIN_U16("graphics/ichor/tablet_back.gbapal");

// Zero means closed; open windows are stored as their id plus one.
static EWRAM_DATA u8 sScenePictureWindow = 0;
static EWRAM_DATA u8 sActOneCardWindow = 0;
static EWRAM_DATA u16 sPictureUnfadedPalette[16] = {0};
static EWRAM_DATA u16 sPictureFadedPalette[16] = {0};
static EWRAM_DATA u16 sCardUnfadedPalettes[32] = {0};
static EWRAM_DATA u16 sCardFadedPalettes[32] = {0};

bool32 Ichor_ShowScenePicture(const u8 *tiles, const u16 *palette)
{
    const struct WindowTemplate template =
    {
        .bg = 0, .tilemapLeft = 2, .tilemapTop = 1,
        .width = 8, .height = 8, .paletteNum = 13, .baseBlock = 100,
    };
    u32 window;
    if (sScenePictureWindow != 0 || sActOneCardWindow != 0)
        return FALSE;
    window = AddWindow(&template);
    if (window == WINDOW_NONE)
        return FALSE;
    sScenePictureWindow = window + 1;
    memcpy(sPictureUnfadedPalette, &gPlttBufferUnfaded[BG_PLTT_ID(13)], sizeof(sPictureUnfadedPalette));
    memcpy(sPictureFadedPalette, &gPlttBufferFaded[BG_PLTT_ID(13)], sizeof(sPictureFadedPalette));
    LoadPalette(palette, BG_PLTT_ID(13), PLTT_SIZE_4BPP);
    CopyToWindowPixelBuffer(window, tiles, 2048, 0);
    PutWindowTilemap(window);
    CopyWindowToVram(window, COPYWIN_FULL);
    return TRUE;
}

void Ichor_HideScenePicture(void)
{
    u32 window;
    if (sScenePictureWindow == 0)
        return;
    window = sScenePictureWindow - 1;
    ClearWindowTilemap(window);
    CopyWindowToVram(window, COPYWIN_MAP);
    RemoveWindow(window);
    LoadPalette(sPictureUnfadedPalette, BG_PLTT_ID(13), sizeof(sPictureUnfadedPalette));
    memcpy(&gPlttBufferFaded[BG_PLTT_ID(13)], sPictureFadedPalette, sizeof(sPictureFadedPalette));
    ScheduleBgCopyTilemapToVram(0);
    sScenePictureWindow = 0;
}

u16 Ichor_ShowTabletPicture(void)
{
    return Ichor_ShowScenePicture((const u8 *)sTabletPicture, sTabletPalette);
}

u16 Ichor_ShowActOneCard(void)
{
    const struct WindowTemplate template =
    {
        .bg = 0, .tilemapLeft = 1, .tilemapTop = 3,
        .width = 28, .height = 12, .paletteNum = 15, .baseBlock = 100,
    };
    const u8 *heading = COMPOUND_STRING("END OF ACT I");
    const u8 *subtitle = COMPOUND_STRING("THE UNWOVEN");
    const u8 *controls = COMPOUND_STRING("A/B: Continue");
    u32 window;
    if (sScenePictureWindow != 0 || sActOneCardWindow != 0)
        return FALSE;
    window = AddWindow(&template);
    if (window == WINDOW_NONE)
        return FALSE;
    sActOneCardWindow = window + 1;
    memcpy(sCardUnfadedPalettes, &gPlttBufferUnfaded[BG_PLTT_ID(14)], sizeof(sCardUnfadedPalettes));
    memcpy(sCardFadedPalettes, &gPlttBufferFaded[BG_PLTT_ID(14)], sizeof(sCardFadedPalettes));
    LoadPalette(gStandardMenuPalette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    LoadWindowGfx(window, 0, 0x214, BG_PLTT_ID(14));
    DrawStdFrameWithCustomTileAndPalette(window, FALSE, 0x214, 14);
    AddTextPrinterParameterized(window, FONT_NORMAL, heading,
        GetStringCenterAlignXOffset(FONT_NORMAL, heading, 224), 17, TEXT_SKIP_DRAW, NULL);
    AddTextPrinterParameterized(window, FONT_NORMAL, subtitle,
        GetStringCenterAlignXOffset(FONT_NORMAL, subtitle, 224), 43, TEXT_SKIP_DRAW, NULL);
    AddTextPrinterParameterized(window, FONT_SMALL, controls,
        GetStringCenterAlignXOffset(FONT_SMALL, controls, 224), 77, TEXT_SKIP_DRAW, NULL);
    CopyWindowToVram(window, COPYWIN_FULL);
    return TRUE;
}

void Ichor_HideActOneCard(void)
{
    u32 window;
    if (sActOneCardWindow == 0)
        return;
    window = sActOneCardWindow - 1;
    ClearStdWindowAndFrameToTransparent(window, TRUE);
    RemoveWindow(window);
    LoadPalette(sCardUnfadedPalettes, BG_PLTT_ID(14), sizeof(sCardUnfadedPalettes));
    memcpy(&gPlttBufferFaded[BG_PLTT_ID(14)], sCardFadedPalettes, sizeof(sCardFadedPalettes));
    ScheduleBgCopyTilemapToVram(0);
    sActOneCardWindow = 0;
}

// Force the day-night tint to an hour, for a scene that must play at night
// whatever the clock says (beat 10's night leg). VAR_0x8004 is the hour,
// 1-23; 0 hands the tint back to the real clock. The engine stores 0 as "no
// override", so midnight itself can't be forced: use 23 or 1.
void Ichor_SetHoursOverride(void)
{
    SetTimeOfDay(gSpecialVar_0x8004 % 24);
}
