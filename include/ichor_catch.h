#ifndef GUARD_ICHOR_CATCH_H
#define GUARD_ICHOR_CATCH_H

// The catch mash: tap A as you throw for a small, capped catch bonus.
// Numbers in include/config/ichor.h; notes in design/ENGINE_API.md §12.

// The window's state. Global so tests and the headless check can read it.
struct IchorCatchMash
{
    u8 open;
    u8 timer;      // frames since the window opened
    u8 presses;    // A presses counted this throw, up to ICHOR_CATCH_MASH_CAP
    u8 linger;     // frames shown after the last pip filled
    u16 baseOdds;  // the last throw's modified catch rate, before the bonus
    u16 finalOdds; // and after it
};
extern struct IchorCatchMash gIchorCatchMash;

// The pure math: odds (the modified catch rate) raised by `presses`, capped.
// Zero presses returns odds unchanged. Odds above ICHOR_CATCH_MASH_ODDS_CEILING
// (auto-catches, Master Balls) are never touched, and boosted odds never pass it.
u32 Ichor_ApplyCatchMash(u32 odds, u32 presses);

// Called every frame by Cmd_handleballthrow before the odds are rolled.
// `eligible` says whether this throw can get a window; it is read only when a
// window would open. Returns TRUE while the window is open (keep waiting).
bool32 Ichor_CatchMashWait(bool32 eligible);
bool32 Ichor_CatchMashIsOpen(void);

// Applies the presses from the window that just closed, then clears them, so a
// throw without a window (the victory catch, a later throw) never inherits them.
u32 Ichor_TakeCatchMash(u32 odds);

#endif // GUARD_ICHOR_CATCH_H
