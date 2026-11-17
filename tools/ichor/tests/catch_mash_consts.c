#include "engine_consts.h"
#include "battle.h"
#include "ichor_catch.h"
#include "item_menu.h"
#include "constants/battle.h"
#include "constants/items.h"
K(ITEM_POKE_BALL, ITEM_POKE_BALL)
K(ITEM_MASTER_BALL, ITEM_MASTER_BALL)
K(POCKETS_COUNT, POCKETS_COUNT)
K(POCKET_POKE_BALLS, POCKET_POKE_BALLS)
K(OFF_BAG_POSITION_POCKET, offsetof(struct BagPosition, pocket))
K(B_OUTCOME_CAUGHT, B_OUTCOME_CAUGHT)
K(OFF_MASH_OPEN, offsetof(struct IchorCatchMash, open))
K(OFF_MASH_PRESSES, offsetof(struct IchorCatchMash, presses))
K(OFF_MASH_BASE, offsetof(struct IchorCatchMash, baseOdds))
K(OFF_MASH_FINAL, offsetof(struct IchorCatchMash, finalOdds))
K(MASH_CAP, ICHOR_CATCH_MASH_CAP)
K(MASH_MAX_BONUS, ICHOR_CATCH_MASH_MAX_BONUS)
K(MASH_CEILING, ICHOR_CATCH_MASH_ODDS_CEILING)
K(MASH_FRAMES, ICHOR_CATCH_MASH_FRAMES)
