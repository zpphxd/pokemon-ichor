// Constants for tools/ichor/tests/thyrsa_city.lua, on top of slice_consts.c's.
// thyrsa_city.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/map_groups.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

K(MAP_THYRSA_CITY, MAP_THYRSA_CITY)
K(MAP_THYRSA_THEATER, MAP_THYRSA_THEATER)
K(WARP_ID_NONE, WARP_ID_NONE)
K(TRAINER_OINOPION, TRAINER_ICHOR_OINOPION)
K(TRAINER_LENAIA, TRAINER_ICHOR_LENAIA)
K(TRAINER_HEGELOCHOS, TRAINER_ICHOR_HEGELOCHOS)
K(SPECIES_TEST, SPECIES_PRINPLUP)
K(MOVE_TEST, MOVE_SURF)
K(MOVE_NONE, MOVE_NONE)

// The story flags the city reads and sets
K(FLAG_ACT2_BEGUN, FLAG_ICHOR_ACT2_BEGUN)
K(FLAG_ARRIVED, FLAG_ICHOR_ARRIVED_THYRSA)
K(FLAG_VISITED, FLAG_ICHOR_VISITED_THYRSA)
K(FLAG_MET_MANTO, FLAG_ICHOR_MET_MANTO)
K(FLAG_DIONYSIA_DONE, FLAG_ICHOR_DIONYSIA_DONE)
K(FLAG_GIRDLE, FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES)
K(FLAG_DRUM_MOVED, FLAG_ICHOR_NEISTAN_DRUM_MOVED)
K(FLAG_ALETHEA_WENT_WEST, FLAG_ICHOR_ALETHEA_WENT_WEST)
K(FLAG_OMEN_TOLD, FLAG_ICHOR_OMEN_THYRSIVY_TOLD)
K(FLAG_DECOY, FLAG_ICHOR_THEOXENIA_START + 0x21)
K(FLAG_BADGE04_GET, FLAG_BADGE04_GET)
K(FLAG_HIDDEN_HEART_SCALE, FLAG_ICHOR_HIDDEN_THYRSA_HEART_SCALE)
K(FLAG_HIDDEN_CELL_BATTERY, FLAG_ICHOR_HIDDEN_THYRSA_CELL_BATTERY)
K(FLAG_HIDDEN_RARE_CANDY, FLAG_ICHOR_HIDDEN_THYRSA_RARE_CANDY)
K(FLAG_HIDDEN_PRETTY_FEATHER, FLAG_ICHOR_HIDDEN_THYRSA_PRETTY_FEATHER)
K(ICHOR_GOD_ZEUS, ICHOR_GOD_ZEUS)

// IchorSave, where the bank flags live
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
K(OFF_ICHOR_FAVOR, offsetof(struct IchorSave, favor))
