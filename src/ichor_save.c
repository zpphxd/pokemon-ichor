// Ichor: IchorSave, the one block of Ichor state in SaveBlock3, and its flag
// and var banks. See include/ichor_save.h and design/ENGINE_API.md.
#include "global.h"
#include "event_data.h"
#include "ichor_save.h"

// The layout is part of the save format. These pin it, so a change that moves
// a field fails the build instead of silently breaking saves.
STATIC_ASSERT(sizeof(struct IchorSave) == ICHOR_SAVE_SIZE, IchorSaveSize);
STATIC_ASSERT(sizeof(struct IchorThreadAnchor) == 8, IchorThreadAnchorSize);
STATIC_ASSERT(sizeof(struct IchorThread) == 688, IchorThreadSize);
STATIC_ASSERT(offsetof(struct IchorSave, blessing) == 0x008, IchorSaveBlessingOffset);
STATIC_ASSERT(offsetof(struct IchorSave, favor) == 0x010, IchorSaveFavorOffset);
STATIC_ASSERT(offsetof(struct IchorSave, vars) == 0x040, IchorSaveVarsOffset);
STATIC_ASSERT(offsetof(struct IchorSave, flags) == 0x080, IchorSaveFlagsOffset);
STATIC_ASSERT(offsetof(struct IchorSave, dailyFlags) == 0x180, IchorSaveDailyFlagsOffset);
STATIC_ASSERT(offsetof(struct IchorSave, thread) == 0x1A0, IchorSaveThreadOffset);
STATIC_ASSERT(offsetof(struct IchorSave, reserved) == 0x450, IchorSaveReservedOffset);
STATIC_ASSERT(offsetof(struct SaveBlock3, ichor) == 0, IchorSaveFirstInSaveBlock3);
STATIC_ASSERT(ICHOR_FLAGS_START % 8 == 0 && ICHOR_DAILY_FLAGS_START % 8 == 0, IchorFlagBanksByteAligned);
STATIC_ASSERT(FLAGS_COUNT <= ICHOR_FLAGS_START, VanillaFlagsBelowIchorBanks);
STATIC_ASSERT(ICHOR_FLAGS_END < ICHOR_DAILY_FLAGS_START && ICHOR_DAILY_FLAGS_END < SPECIAL_FLAGS_START, IchorFlagBanksFit);
STATIC_ASSERT(ICHOR_VARS_START > VARS_END && ICHOR_VARS_END < SPECIAL_VARS_START, IchorVarBankFits);

#define ICHOR_MOM_LOSSES_START 212  // SYSTEMS §9: "Record against Mom: 0 wins, 212 losses"

// The state every new game, and every save from before IchorSave, starts with.
static void SetDefaults(void)
{
    memset(&gIchorSave, 0, sizeof(gIchorSave));
    gIchorSave.version = ICHOR_SAVE_VERSION;
    gIchorSave.momLosses = ICHOR_MOM_LOSSES_START;
}

void Ichor_InitSave(void)
{
    SetDefaults();
}

// Called once a save has loaded. A save made before IchorSave existed has zeros
// here (save.c zeroes every sector before writing it), so version 0 gets the
// new-game defaults. Later versions add a step for each field they carve out of
// `reserved`.
void Ichor_OnSaveLoaded(void)
{
    if (gIchorSave.version == 0)
    {
        SetDefaults();
        return;
    }
    if (gIchorSave.version < 2)
    {
        gIchorSave.frozenHourStep = 0;
        gIchorSave.version = 2;
    }
}

void Ichor_DoDailyEvents(u32 daysSince)
{
    memset(gIchorSave.dailyFlags, 0, sizeof(gIchorSave.dailyFlags));
}

u8 *Ichor_GetFlagPointer(u16 id)
{
    if (id >= ICHOR_FLAGS_START && id <= ICHOR_FLAGS_END)
        return &gIchorSave.flags[(id - ICHOR_FLAGS_START) / 8];
    if (id >= ICHOR_DAILY_FLAGS_START && id <= ICHOR_DAILY_FLAGS_END)
        return &gIchorSave.dailyFlags[(id - ICHOR_DAILY_FLAGS_START) / 8];
    return NULL;
}

u16 *Ichor_GetVarPointer(u16 id)
{
    if (id >= ICHOR_VARS_START && id <= ICHOR_VARS_END)
        return &gIchorSave.vars[id - ICHOR_VARS_START];
    return NULL;
}

// How many of the `count` flags from `firstFlag` on are set: herms anointed,
// sherds found, constellations placed. Works on any flag range, not only the bank.
u32 Ichor_CountFlags(u16 firstFlag, u16 count)
{
    u32 i, n = 0;

    for (i = 0; i < count; i++)
    {
        if (FlagGet(firstFlag + i))
            n++;
    }
    return n;
}
