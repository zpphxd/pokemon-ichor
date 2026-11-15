// Ichor: the Nurseries' monthly tables (design/OIKOUMENE.md §8; design/oikoumene/BUILD.md
// §5, "The Nurseries' monthly tables"). A Nursery map keeps one wild_encounters.json
// entry per Aethos month and GetCurrentMapWildMonHeaderId reads this month's. These
// check the month and the offset into a map's run of entries; batch 2's first
// Nursery map adds an in-game check (tools/ichor/tests/).
#include "global.h"
#include "event_data.h"
#include "wild_encounter.h"
#include "test/test.h"
#include "constants/maps.h"
#include "constants/vars.h"

TEST("Ichor: the Aethos month is twelve months of three days on the day count")
{
    VarSet(VAR_DAYS, 0);
    EXPECT_EQ(Ichor_GetAethosMonth(), 0);
    VarSet(VAR_DAYS, 2);
    EXPECT_EQ(Ichor_GetAethosMonth(), 0);
    VarSet(VAR_DAYS, 3);
    EXPECT_EQ(Ichor_GetAethosMonth(), 1);
    VarSet(VAR_DAYS, 35);
    EXPECT_EQ(Ichor_GetAethosMonth(), 11);
    VarSet(VAR_DAYS, 36);
    EXPECT_EQ(Ichor_GetAethosMonth(), 0);
    VarSet(VAR_DAYS, 36 * 5 + 22);
    EXPECT_EQ(Ichor_GetAethosMonth(), 7);
}

static void FillHeaders(struct WildPokemonHeader *headers, u32 count, u32 mapGroup, u32 mapNum)
{
    for (u32 i = 0; i < count; i++)
    {
        headers[i].mapGroup = mapGroup;
        headers[i].mapNum = mapNum;
    }
}

TEST("Ichor: a Nursery's twelve entries give each month its own table")
{
    static struct WildPokemonHeader headers[14];
    memset(headers, 0, sizeof(headers));
    FillHeaders(&headers[0], 12, 3, 7);             // the Nursery: twelve in a row
    FillHeaders(&headers[12], 1, 3, 8);             // the next map's
    headers[13].mapGroup = MAP_GROUP(MAP_UNDEFINED); // the end
    for (u32 month = 0; month < 12; month++)
        EXPECT_EQ(Ichor_GetNurseryHeaderOffset(headers, 0, month), month);
}

TEST("Ichor: a Nursery with fewer than twelve entries wraps the month, and one entry is always read")
{
    static struct WildPokemonHeader headers[6];
    memset(headers, 0, sizeof(headers));
    FillHeaders(&headers[0], 3, 3, 7);              // three tables
    FillHeaders(&headers[3], 1, 3, 9);              // one table
    FillHeaders(&headers[4], 1, 3, 10);
    headers[5].mapGroup = MAP_GROUP(MAP_UNDEFINED);
    EXPECT_EQ(Ichor_GetNurseryHeaderOffset(headers, 0, 7), 1);
    EXPECT_EQ(Ichor_GetNurseryHeaderOffset(headers, 0, 11), 2);
    EXPECT_EQ(Ichor_GetNurseryHeaderOffset(headers, 3, 11), 0);
}

TEST("Ichor: a map that isn't a Nursery reads its one table, whatever the month")
{
    VarSet(VAR_DAYS, 3 * 9);
    for (u32 i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
        EXPECT(Ichor_IsWildHeaderCurrent(i));
}
