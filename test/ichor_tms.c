#include "global.h"
#include "item.h"
#include "pokemon.h"
#include "test/test.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/species.h"

TEST("Ichor: Act I scrolls map to their moves without moving existing items")
{
    EXPECT_EQ(ITEM_TM_FLING, ITEM_TM51);
    EXPECT_EQ(ITEM_TM_BULLDOZE, ITEM_TM52);
    EXPECT_EQ(ITEM_TM_ROUND, ITEM_TM53);
    EXPECT_EQ(ITEM_HM01, 682);
    EXPECT_EQ(GetItemTMHMMoveId(ITEM_TM17), MOVE_PROTECT);
    EXPECT_EQ(GetItemTMHMMoveId(ITEM_TM_FLING), MOVE_FLING);
    EXPECT_EQ(GetItemTMHMMoveId(ITEM_TM_BULLDOZE), MOVE_BULLDOZE);
    EXPECT_EQ(GetItemTMHMMoveId(ITEM_TM_ROUND), MOVE_ROUND);
    EXPECT_EQ(GetItemTMHMMoveId(ITEM_HM01), MOVE_CUT);
    EXPECT_LE(NUM_ALL_MACHINES, BAG_TMHM_COUNT);
    EXPECT_EQ(BAG_TMHM_COUNT, 64);
}

TEST("Ichor: Act I scrolls teach eligible regional species")
{
    EXPECT(CanLearnTeachableMove(SPECIES_SPALUNK, MOVE_FLING));
    EXPECT(CanLearnTeachableMove(SPECIES_PLOUTERAS, MOVE_FLING));
    EXPECT(CanLearnTeachableMove(SPECIES_THALAMARE, MOVE_BULLDOZE));
    EXPECT(CanLearnTeachableMove(SPECIES_HARPECK, MOVE_ROUND));
    EXPECT(!CanLearnTeachableMove(SPECIES_KAPLET, MOVE_FLING));
    EXPECT(!CanLearnTeachableMove(SPECIES_MAGIKARP, MOVE_FLING));
}

TEST("Ichor: dynamically selected rite lessons keep species eligibility")
{
    EXPECT(CanLearnTeachableMove(SPECIES_HARPECK, MOVE_U_TURN));
    EXPECT(CanLearnTeachableMove(SPECIES_KORANTHA, MOVE_LEECH_SEED));
    EXPECT(!CanLearnTeachableMove(SPECIES_NEBREL, MOVE_U_TURN));
    EXPECT(!CanLearnTeachableMove(SPECIES_MAGIKARP, MOVE_U_TURN));
}
