#include "engine_consts.h"
#include "battle.h"
#include "ichor_oath.h"
#include "item_menu.h"
#include "pokemon_storage_system.h"
#include "constants/battle.h"
#include "constants/items.h"
K(OFF_OATH, offsetof(struct IchorSave, oath))
K(OFF_OATH_STATE, offsetof(struct IchorOath, state))
K(OFF_OATH_ENCOUNTERS, offsetof(struct IchorOath, encounters))
K(OFF_OATH_URN_BOXES, offsetof(struct IchorOath, urnBoxes))
K(ICHOR_OATH_ACTIVE, ICHOR_OATH_ACTIVE)
K(ICHOR_OATH_RELEASED, ICHOR_OATH_RELEASED)
K(TOTAL_BOXES_COUNT, TOTAL_BOXES_COUNT)
K(ITEM_MASTER_BALL, ITEM_MASTER_BALL)
K(POCKETS_COUNT, POCKETS_COUNT)
K(POCKET_POKE_BALLS, POCKET_POKE_BALLS)
K(OFF_BAG_POSITION_POCKET, offsetof(struct BagPosition, pocket))
K(B_OUTCOME_CAUGHT, B_OUTCOME_CAUGHT)
K(B_OUTCOME_RAN, B_OUTCOME_RAN)
K(OFF_BATTLE_TURN, offsetof(struct BattleResults, battleTurnCounter))
