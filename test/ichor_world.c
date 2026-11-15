// Ichor: scripts' small needs (design/ENGINE_API.md §7): counting a flag range,
// a forced omen, holding the day-and-night tint; and carried flames (§2).
#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "ichor_relics.h"
#include "ichor_save.h"
#include "rtc.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/rtc.h"

u16 Ichor_CountFlagRange(void);
void Ichor_ForceOmen(void);
u16 Ichor_CheckOmen(void);
u16 Ichor_GetOmen(void);
void Ichor_HoldTimeOfDay(void);
void Ichor_ReleaseTimeOfDay(void);

TEST("Ichor: Ichor_CountFlagRange counts the set flags in a range")
{
    u32 i;
    for (i = 0; i < 8; i++)
        FlagClear(FLAG_ICHOR_PROPHECY_START + i);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 0);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 3);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 7);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 8);  // outside the range
    gSpecialVar_0x8004 = FLAG_ICHOR_PROPHECY_START;
    gSpecialVar_0x8005 = 8;
    EXPECT_EQ(Ichor_CountFlagRange(), 3);
    FlagClear(FLAG_ICHOR_PROPHECY_START + 8);
}

TEST("Ichor: a forced omen arrives the next day, then the day after has none")
{
    gIchorSave.omenKind = OMEN_NONE;
    gIchorSave.omenEntry = 0;
    gSpecialVar_0x8004 = OMEN_WEATHER;
    gSpecialVar_0x8005 = OMEN_WEATHER_LERNIP;
    Ichor_ForceOmen();
    EXPECT_EQ(Ichor_CheckOmen(), FALSE);  // not today

    Ichor_DoDailyEvents(1);
    gSpecialVar_0x8004 = OMEN_WEATHER;
    gSpecialVar_0x8005 = OMEN_WEATHER_LERNIP;
    EXPECT_EQ(Ichor_CheckOmen(), TRUE);
    gSpecialVar_0x8005 = OMEN_WEATHER_KRYOPUFF;
    EXPECT_EQ(Ichor_CheckOmen(), FALSE);
    EXPECT_EQ(Ichor_GetOmen(), OMEN_WEATHER);
    EXPECT_EQ(gSpecialVar_0x8004, OMEN_WEATHER_LERNIP);

    Ichor_DoDailyEvents(1);
    EXPECT_EQ(Ichor_GetOmen(), OMEN_NONE);
}

TEST("Ichor: a held time of day overrides the clock until released")
{
    u32 time;
    for (time = 0; time < TIMES_OF_DAY_COUNT; time++)
    {
        gSpecialVar_0x8004 = time;
        Ichor_HoldTimeOfDay();
        EXPECT_EQ(GetTimeOfDay(), time);
    }
    Ichor_ReleaseTimeOfDay();
    EXPECT_EQ(gIchorSave.heldTimeOfDay, 0);
}

TEST("Ichor: a carried flame counts down even on a quiet step, and water puts it out")
{
    VarSet(VAR_TEMP_2, 10);
    VarSet(VAR_TEMP_3, FLAME_HEARTH);
    EXPECT_EQ(Ichor_CarriedFlameStep(FALSE), FALSE);
    EXPECT_EQ(VarGet(VAR_TEMP_2), 9);
    EXPECT_EQ(VarGet(VAR_TEMP_3), FLAME_HEARTH);

    gPlayerAvatar.flags |= PLAYER_AVATAR_FLAG_SURFING;
    EXPECT_EQ(Ichor_CarriedFlameStep(FALSE), FALSE);
    EXPECT_EQ(VarGet(VAR_TEMP_3), FLAME_NONE);
    EXPECT_EQ(Ichor_IsCarryingFlame(), FALSE);
    gPlayerAvatar.flags &= ~PLAYER_AVATAR_FLAG_SURFING;
}
