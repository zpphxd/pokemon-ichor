// The catch mash (design/ENGINE_API.md §12, numbers in include/config/ichor.h).
//
// The expansion rolls a throw's shakes in Cmd_handleballthrow, before the throw
// animation plays. Rather than re-rolling shakes during the animation, the window
// opens first: after "{PLAYER} used Poké Ball!" prints, the second line of the
// message box shows a blinking "Tap A!" and a row of pips. Each A press fills a
// pip. The window closes after ICHOR_CATCH_MASH_FRAMES, or a beat after the last
// pip fills, and only then are the odds rolled, with the bonus included. The
// animation that follows shows exactly that roll.
#include "global.h"
#include "battle.h"
#include "ichor_catch.h"
#include "main.h"
#include "menu.h"
#include "sound.h"
#include "string_util.h"
#include "test_runner.h"
#include "text.h"
#include "window.h"
#include "constants/battle.h"
#include "constants/songs.h"

#define PROMPT_LINE_Y   16  // the message box's second line
#define PIPS_X          48  // where the pips start, clear of "Tap A!"
#define BLINK_FRAMES    12  // half a blink of the prompt, until the first press
#define LINGER_FRAMES   10  // how long the full row shows before the throw

EWRAM_DATA struct IchorCatchMash gIchorCatchMash = {0};

static const u8 sText_Tap[] = _("Tap {A_BUTTON}!");
static const u8 sText_PipFull[] = _("{STAR}");
static const u8 sText_PipEmpty[] = _("·");

u32 Ichor_ApplyCatchMash(u32 odds, u32 presses)
{
    if (odds > ICHOR_CATCH_MASH_ODDS_CEILING)
        return odds;
    if (presses > ICHOR_CATCH_MASH_CAP)
        presses = ICHOR_CATCH_MASH_CAP;
    odds = odds * (100 * ICHOR_CATCH_MASH_CAP + ICHOR_CATCH_MASH_MAX_BONUS * presses)
                / (100 * ICHOR_CATCH_MASH_CAP);
    if (odds > ICHOR_CATCH_MASH_ODDS_CEILING)
        odds = ICHOR_CATCH_MASH_ODDS_CEILING;
    return odds;
}

static void DrawPrompt(bool32 showTap)
{
    // B_WIN_MSG's own colors (sTextOnWindowsInfo_Normal): background, foreground, shadow.
    static const u8 sColors[] = {15, 1, 6};
    u8 pips[ICHOR_CATCH_MASH_CAP * 2 + 1];
    u32 i;
    u32 width = GetWindowAttribute(B_WIN_MSG, WINDOW_WIDTH) * TILE_WIDTH;
    u32 height = GetWindowAttribute(B_WIN_MSG, WINDOW_HEIGHT) * TILE_HEIGHT;

    pips[0] = EOS;
    for (i = 0; i < ICHOR_CATCH_MASH_CAP; i++)
        StringAppend(pips, i < gIchorCatchMash.presses ? sText_PipFull : sText_PipEmpty);

    FillWindowPixelRect(B_WIN_MSG, PIXEL_FILL(0xF), 0, PROMPT_LINE_Y, width, height - PROMPT_LINE_Y);
    if (showTap)
        AddTextPrinterParameterized3(B_WIN_MSG, FONT_NORMAL, 0, PROMPT_LINE_Y + 1, sColors, TEXT_SKIP_DRAW, sText_Tap);
    AddTextPrinterParameterized3(B_WIN_MSG, FONT_NORMAL, PIPS_X, PROMPT_LINE_Y + 1, sColors, TEXT_SKIP_DRAW, pips);
    CopyWindowToVram(B_WIN_MSG, COPYWIN_GFX);
}

bool32 Ichor_CatchMashIsOpen(void)
{
    return gIchorCatchMash.open;
}

bool32 Ichor_CatchMashWait(bool32 eligible)
{
    if (!gIchorCatchMash.open)
    {
        gIchorCatchMash.presses = 0;
        // Nobody holds the pad in the test runner, a link or a recorded battle.
        if (!ICHOR_CATCH_MASH || !eligible || gTestRunnerEnabled
         || (gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED)))
            return FALSE;
        gIchorCatchMash.open = TRUE;
        gIchorCatchMash.timer = 0;
        gIchorCatchMash.linger = 0;
        DrawPrompt(TRUE);
        return TRUE;
    }

    gIchorCatchMash.timer++;
    if (gIchorCatchMash.presses < ICHOR_CATCH_MASH_CAP && JOY_NEW(A_BUTTON))
    {
        gIchorCatchMash.presses++;
        PlaySE(SE_BALL_TRAY_BALL);
        DrawPrompt(TRUE);
    }
    else if (gIchorCatchMash.presses == 0 && gIchorCatchMash.timer % BLINK_FRAMES == 0)
    {
        DrawPrompt((gIchorCatchMash.timer / BLINK_FRAMES) % 2 == 0);
    }

    if (gIchorCatchMash.presses >= ICHOR_CATCH_MASH_CAP)
        gIchorCatchMash.linger++;
    if (gIchorCatchMash.timer >= ICHOR_CATCH_MASH_FRAMES || gIchorCatchMash.linger >= LINGER_FRAMES)
    {
        gIchorCatchMash.open = FALSE;
        return FALSE;
    }
    return TRUE;
}

u32 Ichor_TakeCatchMash(u32 odds)
{
    u32 boosted = Ichor_ApplyCatchMash(odds, gIchorCatchMash.presses);

    gIchorCatchMash.baseOdds = min(odds, 0xFFFF);
    gIchorCatchMash.finalOdds = min(boosted, 0xFFFF);
    gIchorCatchMash.presses = 0;
    return boosted;
}
