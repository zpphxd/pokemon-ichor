#!/usr/bin/env bash
# Eleusa's six interiors check: every room's event, played with key presses.
#
#   tools/ichor/tests/eleusa_rooms.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Modeled on emporion_rooms.sh (the events) with eleusa.sh's walker: Quickstarts,
# gives a lead and the Melibee Euphorion wants, warps to the road below the
# Asclepeion's door, and then walks into each room through its door, plays it,
# and walks back out onto its door's tile in the village:
#   1. the Asclepeion: the healer across the counter, the respawn, the Pithos,
#      the Panacoil, the pilgrim and the farmer, and the readable things;
#   2. the Agora stall: the shop's item list opened and closed, the customer;
#   3. the granary-keeper's house: Sitokles's lore, then after the theft the
#      Amulet Coin; the Revive under the bed;
#   4. Euphorion's house: the trade of the Melibee for CRITIC, the Melibee on
#      the stage after it, and the new ending after Act I;
#   5. Dysaules's farmhouse: Theano's TM09 Bullet Seed, the Galekit;
#   6. the house of Keleos: Metaneira's table heals, the rest by the hearth, and
#      after the Harvest Laurel the goddess's drink.
# Output in build/test_eleusa_rooms/ (screenshots in shots/); see eleusa_rooms.lua.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_eleusa_rooms
engine_prepare ELEUSA_ROOMS "$OUT" tools/ichor/tests/eleusa_rooms_consts.c ""
# The rooms' scripts by name (slice_symbols.sh lists Eleusa's already), and the
# few addresses the walk reads besides.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(CB2_PokeStorage)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/eleusa_rooms_symbols.lua"
engine_run ELEUSA_ROOMS "$OUT" tools/ichor/tests/eleusa_rooms.lua 400000 1500
