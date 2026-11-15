// Ichor: world-act3's small helpers for Kythera's scripts (design/phase4/SCRIPT.md).
#include "global.h"
#include "ichor_kythera.h"
#include "item.h"
#include "constants/items.h"

#define FIRST_FRUITS 3

// specialvar Ichor_TakeFirstFruits: Krenaia's first fruits at the Neraida falls
// (SCRIPT.md Part 5, "The Silent Falls", step 4). If the bag holds three berries
// of any kind, take three, in bag order, and return TRUE; otherwise take nothing
// and return FALSE.
u16 Ichor_TakeFirstFruits(void)
{
    u32 item, held = 0, need = FIRST_FRUITS;

    for (item = FIRST_BERRY_INDEX; item <= LAST_BERRY_INDEX; item++)
        held += CountTotalItemQuantityInBag(item);
    if (held < FIRST_FRUITS)
        return FALSE;

    for (item = FIRST_BERRY_INDEX; item <= LAST_BERRY_INDEX && need != 0; item++)
    {
        u32 take = CountTotalItemQuantityInBag(item);

        if (take > need)
            take = need;
        if (take != 0)
        {
            RemoveBagItem(item, take);
            need -= take;
        }
    }
    return TRUE;
}
