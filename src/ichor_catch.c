// The catch mash (design/ENGINE_API.md §12, numbers in include/config/ichor.h).
//
// The expansion rolls a throw's shakes in Cmd_handleballthrow, before the throw
// animation plays. Rather than re-rolling shakes during the animation, the window
// opens first: after "{PLAYER} used Poké Ball!" prints, the message holds for up
// to ICHOR_CATCH_MASH_FRAMES while A presses are counted. The window is a secret
// (the user's call): nothing on screen or in the sound hints at it. It closes
// early a beat after the cap is reached, and only then are the odds rolled, with
// the bonus included. The animation that follows shows exactly that roll.
#include "global.h"
#include "battle.h"
#include "ichor_catch.h"
#include "main.h"
#include "test_runner.h"
#include "constants/battle.h"

#define LINGER_FRAMES   10  // the beat after the cap before the throw

EWRAM_DATA struct IchorCatchMash gIchorCatchMash = {0};

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
        return TRUE;
    }

    gIchorCatchMash.timer++;
    if (gIchorCatchMash.presses < ICHOR_CATCH_MASH_CAP && JOY_NEW(A_BUTTON))
        gIchorCatchMash.presses++;

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
