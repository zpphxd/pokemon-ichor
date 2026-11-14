// Constants and offsets every Ichor engine-system check needs. Each check's
// *_consts.c includes this; engine_build.sh compiles it with the game's own
// headers (gcc -S) and turns each k_NAME into a Lua table entry.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// IchorSave (include/ichor_save.h), inside SaveBlock3
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(SB3_SIZE, sizeof(struct SaveBlock3))
K(ICHOR_SAVE_SIZE, sizeof(struct IchorSave))
K(ICHOR_SAVE_VERSION, ICHOR_SAVE_VERSION)
K(OFF_ICHOR_VERSION, offsetof(struct IchorSave, version))
K(OFF_ICHOR_OPTIONS, offsetof(struct IchorSave, options))
K(OFF_ICHOR_RING_CURSOR, offsetof(struct IchorSave, relicRingCursor))
K(OFF_ICHOR_BLESSING, offsetof(struct IchorSave, blessing))
K(OFF_ICHOR_FAVOR, offsetof(struct IchorSave, favor))
K(OFF_ICHOR_MOM_WINS, offsetof(struct IchorSave, momWins))
K(OFF_ICHOR_MOM_LOSSES, offsetof(struct IchorSave, momLosses))
K(OFF_ICHOR_VARS, offsetof(struct IchorSave, vars))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
K(OFF_ICHOR_DAILY_FLAGS, offsetof(struct IchorSave, dailyFlags))
K(OFF_ICHOR_THREAD, offsetof(struct IchorSave, thread))
K(OFF_ICHOR_RESERVED, offsetof(struct IchorSave, reserved))

// the banks
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(ICHOR_DAILY_FLAGS_START, ICHOR_DAILY_FLAGS_START)
K(ICHOR_DAILY_FLAGS_END, ICHOR_DAILY_FLAGS_END)
K(ICHOR_VARS_START, ICHOR_VARS_START)
K(ICHOR_VARS_END, ICHOR_VARS_END)
K(FLAG_ICHOR_GENERAL_START, FLAG_ICHOR_GENERAL_START)
K(FLAG_ICHOR_HERMS_START, FLAG_ICHOR_HERMS_START)
K(FLAG_DAILY_ICHOR_PRAYED_START, FLAG_DAILY_ICHOR_PRAYED_START)
K(FLAG_DAILY_ICHOR_GENERAL_START, FLAG_DAILY_ICHOR_GENERAL_START)

// vanilla state the checks read
K(SPECIAL_VARS_START, SPECIAL_VARS_START)
K(VAR_TEMP_F, VAR_TEMP_F)
K(VAR_DAYS, VAR_DAYS)
K(VAR_RESULT, VAR_RESULT)
K(VAR_0x8000, VAR_0x8000)
K(VAR_0x8001, VAR_0x8001)
K(VAR_0x8002, VAR_0x8002)
K(VAR_0x8004, VAR_0x8004)
K(VAR_0x8005, VAR_0x8005)
K(NUM_FLAG_BYTES, NUM_FLAG_BYTES)
K(OFF_SB2_LOCAL_TIME_OFFSET, offsetof(struct SaveBlock2, localTimeOffset))
K(OFF_SB1_VARS_E, offsetof(struct SaveBlock1, vars))
