// Constants for tools/ichor/tests/act2_arkadia.lua, on top of slice_consts.c's.
// act2_arkadia.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/metatile_labels.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/script_commands.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

K(MAP_ARKADIA, MAP_ARKADIA)
K(MAP_WOOD, MAP_ARKADIA_CYPRESS_WOOD)
K(MAP_POOL, MAP_POOL_OF_MNEMOSYNE)
K(WARP_ID_NONE, WARP_ID_NONE)
K(SCR_OP_CLEARFLAG, SCR_OP_CLEARFLAG)

K(SPECIES_TEST, SPECIES_PRINPLUP)
K(MOVE_TEST, MOVE_SURF)
K(MOVE_NONE, MOVE_NONE)

K(METATILE_LAMP_LIT_L, METATILE_Arkadia_LampLit_L)
K(METATILE_LAMP_LIT_R, METATILE_Arkadia_LampLit_R)
K(METATILE_LAMP_UNLIT_L, METATILE_Arkadia_LampUnlit_L)

K(TRAINER_EUADNE, TRAINER_ICHOR_EUADNE)
K(TRAINER_LYSIPPE, TRAINER_ICHOR_LYSIPPE)
K(TRAINER_MELANIPPE, TRAINER_ICHOR_MELANIPPE)

K(ITEM_TINY_MUSHROOM, ITEM_TINY_MUSHROOM)
K(ITEM_REVIVE, ITEM_REVIVE)
K(ITEM_CHARCOAL, ITEM_CHARCOAL)

// story flags (the Ichor bank)
K(FLAG_ACT2_BEGUN, FLAG_ICHOR_ACT2_BEGUN)
K(FLAG_ARRIVED, FLAG_ICHOR_ARRIVED_ARKADIA)
K(FLAG_VISITED, FLAG_ICHOR_VISITED_ARKADIA)
K(FLAG_KLEON_JOINED, FLAG_ICHOR_KLEON_JOINED_TITANS)
K(FLAG_SKYLAPS, FLAG_ICHOR_ALETHEA_GOT_SKYLAPS)
K(FLAG_TABLET_5, FLAG_ICHOR_PROPHECY_START + 4)
K(FLAG_TABLET_5_READ, FLAG_ICHOR_PROPHECY_START + 12)
K(FLAG_DECOY, FLAG_ICHOR_THEOXENIA_START + 0x25)
K(FLAG_KID_1, FLAG_ICHOR_KROTOS_KID_1)
K(FLAG_MNASEAS_TOLD, FLAG_ICHOR_MNASEAS_TOLD)
K(FLAG_BADGE05_GET, FLAG_BADGE05_GET)

// item flags (vanilla)
K(FLAG_HIDDEN_REVIVE, FLAG_ICHOR_HIDDEN_ARKADIA_REVIVE)
K(FLAG_ITEM_MAX_REPEL, FLAG_ICHOR_ITEM_ARKADIA_MAX_REPEL)
K(FLAG_HIDDEN_CHARCOAL, FLAG_ICHOR_HIDDEN_CYPRESS_WOOD_CHARCOAL)

// IchorSave, where the bank flags live
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
