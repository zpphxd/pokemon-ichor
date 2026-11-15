// Constants for tools/ichor/tests/kithairon.lua, on top of slice_consts.c's.
// kithairon.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id.
#include "global.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/metatile_labels.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

K(MAP_ROUTE6, MAP_ROUTE6_ELEUTHERAI_ROAD)
K(MAP_CAVE, MAP_ROUTE6_ANTIOPES_CAVE)
K(MAP_ELEUTHERAI, MAP_ELEUTHERAI)
K(MAP_KITHAIRON, MAP_MT_KITHAIRON)
K(MAP_ROUTE7, MAP_ROUTE7_KRONIA_GROUNDS)
K(FLAG_SICKLE, FLAG_ICHOR_GOT_DEMETERS_SICKLE)
K(METATILE_ROAD, 0x1D9)
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(FLAG_HIDE_VINES, FLAG_ICHOR_HIDE_ELEUTHERAI_VINES)
K(SPECIES_TEST, SPECIES_PRINPLUP)
K(MOVE_TEST, MOVE_SURF)
K(MOVE_NONE, MOVE_NONE)
K(TRAINER_IKARIOS, TRAINER_ICHOR_IKARIOS)
K(TRAINER_PYTHODOROS, TRAINER_ICHOR_PYTHODOROS)
K(TRAINER_ASTYLOS, TRAINER_ICHOR_ASTYLOS)
K(TRAINER_LYKIDAS, TRAINER_ICHOR_LYKIDAS)
K(TRAINER_EUIA, TRAINER_ICHOR_EUIA)
K(TRAINER_KOMOS, TRAINER_ICHOR_KOMOS)
K(TRAINER_HAGNON, TRAINER_ICHOR_HAGNON)
