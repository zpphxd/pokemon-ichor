#ifndef GUARD_ICHOR_SAVE_H
#define GUARD_ICHOR_SAVE_H

// Ichor: all of Ichor's own persistent state, in one block of SaveBlock3.
//
// The layout is fixed at ICHOR_SAVE_SIZE bytes so later systems take bytes from
// `reserved` instead of growing the block, and saves keep loading. When a field
// is carved out of `reserved`, bump ICHOR_SAVE_VERSION and give the new field
// its default in Ichor_OnSaveLoaded's migration (src/ichor_save.c).
//
// Version 4 grew the block once, by 192 bytes, for a second bank of 1,536 flags
// (SaveBlock3 has room to 1,624 bytes; it now uses 1,476).
//
// Flags and vars: IchorSave also holds two banks of saved flags (2,048 and
// 1,536), 256 daily flags and 32 vars. Scripts use them with the ordinary setflag, checkflag and
// setvar commands: GetFlagPointer and GetVarPointer (src/event_data.c) send
// their ids here. The ids and the named ranges are in include/constants/flags.h
// and vars.h ("Ichor flag bank"), and tools/ichor/claim.py claims them by name.
// See design/ENGINE_API.md.

#include "constants/flags.h"
#include "constants/vars.h"

#define ICHOR_SAVE_VERSION  5
#define ICHOR_SAVE_SIZE     1472

#define ICHOR_GOD_SLOTS     16  // the 15 gods of design/SYSTEMS.md §3, and one spare
#define ICHOR_XENIA_CHAINS  8   // §10: 3 token chains in 1.0, room for more

// LABYRINTH.md §5.1: Ariadne's Thread. Anchors are the bronze rings you tie off
// on; `committed` and `live` hold 2 bits per step (the direction of the step).
#define ICHOR_THREAD_ANCHORS          24
#define ICHOR_THREAD_COMMITTED_BYTES  448  // 1,792 committed steps
#define ICHOR_THREAD_LIVE_BYTES       38   // 152 live steps; the spool is at most 150

// 8 bytes, not LABYRINTH.md's 6: apcs-gnu rounds every struct to 4 bytes.
struct IchorThreadAnchor
{
    u16 mapId;  // (mapGroup << 8) | mapNum
    u8 x, y;
    u16 steps;  // length of the segment that starts here
    u16 reserved;
};

struct IchorThread
{
    struct IchorThreadAnchor anchors[ICHOR_THREAD_ANCHORS];
    u8 anchorCount;
    u8 currentAnchor;
    u16 liveMapId;
    u8 liveX, liveY;
    u8 liveLen;
    u8 padding;
    u8 committed[ICHOR_THREAD_COMMITTED_BYTES];
    u8 live[ICHOR_THREAD_LIVE_BYTES];
    u8 reserved[2];
};

// §3: one blessing at a time, counted in steps like a Repel.
struct IchorBlessing
{
    u8 god;     // an ICHOR_GOD_* id (constants/ichor.h, batch 3); 0 = none
    u8 flags;   // ICHOR_BLESSING_* bits: major or minor, Frenzy, given by Dionysus
    u16 steps;  // steps left
};

struct IchorOath
{
    u8 state;
    u8 reserved;
    u16 fallenCount;
    u8 encounters[32];  // one persistent chance per named map section
    u8 padding[4];
};

struct IchorSave
{
    /*0x000*/ u8 version;               // ICHOR_SAVE_VERSION; 0 means a save made before IchorSave
    /*0x001*/ u8 options;               // ICHOR_OPTION_* bits (the relic prompt, §1)
    /*0x002*/ u8 relicRingCursor;       // §1: the Relic Ring opens on the last entry used
    /*0x003*/ u8 omenKind;              // §6: today's omen
    /*0x004*/ u16 omenEntry;            // §6
    /*0x006*/ u16 festivalsSeen;        // §7: one bit per festival
    /*0x008*/ struct IchorBlessing blessing;
    /*0x00C*/ u16 momWins;              // §9
    /*0x00E*/ u16 momLosses;            // §9: 212 in a new game
    /*0x010*/ u8 favor[ICHOR_GOD_SLOTS];        // §3: 0-100 per god, never decreases
    /*0x020*/ u8 xenia[ICHOR_XENIA_CHAINS];     // §10: links done per token chain
    /*0x028*/ u8 frozenHourStep;        // the Frozen Hour: steps of the Stair climbed, 0-11 (version 2)
    /*0x029*/ u8 forcedOmenKind;        // §6: tomorrow's omen, forced by a script; OMEN_NONE if not (version 3)
    /*0x02A*/ u8 forcedOmenEntry;
    /*0x02B*/ u8 heldTimeOfDay;         // a script holds the day-and-night tint: TIME_* + 1, or 0 (version 3)
    /*0x02C*/ u8 headerReserved[20];
    /*0x040*/ u16 vars[ICHOR_VARS_COUNT];
    /*0x080*/ u8 flags[ICHOR_FLAGS_COUNT / 8];
    /*0x180*/ u8 dailyFlags[ICHOR_DAILY_FLAGS_COUNT / 8];  // cleared each day
    /*0x1A0*/ struct IchorThread thread;   // 688 bytes
    /*0x450*/ struct IchorOath oath;     // version 5, carved from reserved bytes
    /*0x478*/ u8 reserved[0x500 - 0x478];
    /*0x500*/ u8 flags2[ICHOR_FLAGS2_COUNT / 8];  // the second flag bank (version 4)
};

#define gIchorSave (gSaveBlock3Ptr->ichor)

// A hidden item's flag, from the 13-bit id bg_hidden_item_event packs
// (asm/macros/map.inc): a vanilla flag's offset, or a bank flag past 0x1000.
static inline u16 Ichor_GetHiddenItemFlag(u32 hiddenItemId)
{
    if (hiddenItemId >= ICHOR_HIDDEN_ITEM_BANK_ID)
        return ICHOR_FLAGS_START + (hiddenItemId - ICHOR_HIDDEN_ITEM_BANK_ID);
    return FLAG_HIDDEN_ITEMS_START + hiddenItemId;
}

void Ichor_InitSave(void);
void Ichor_OnSaveLoaded(void);
void Ichor_DoDailyEvents(u32 daysSince);
u8 *Ichor_GetFlagPointer(u16 id);
u16 *Ichor_GetVarPointer(u16 id);
u32 Ichor_CountFlags(u16 firstFlag, u16 count);

#endif // GUARD_ICHOR_SAVE_H
