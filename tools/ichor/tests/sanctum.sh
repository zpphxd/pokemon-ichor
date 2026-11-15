#!/usr/bin/env bash
# The Mystery sanctum under Eleusa (beat 23), played with key presses:
#
#   tools/ichor/tests/sanctum.sh [rom] < /dev/null    (default: pokeemerald.gba; run make first)
#
# Quickstarts, sets what beats 20-22 leave behind (a party at Eleusa's levels, three
# Laurels, Hecate's Torch, the Lesser Mysteries done, the sanctum open) and lands at
# the foot of the Anaktoron's stair on B1F. Then plays 23A (Chloe holds the stair and
# heals, Alethea takes the lamp grunt), lights the granaries' braziers, fights Bolos and
# Krokalos, takes the items; on B2F hears Hyperion's voice, falls into a grain pit,
# crosses on the chalk, reads the four frescoes in order, rests at the spring, fights
# Konis and Gaios; on B3F reads the sickle, plays the theft and beats Hyperion (to
# MUS_ICHOR_BATTLE_ADMIN), takes Demeter's Sickle and lands on the Telesterion's steps.
# Then goes back down: the tunnel caved in, a wild battle to the ordinary wild music,
# and the climb up all three floors and out by the Anaktoron's stair.
# Output in build/test_sanctum/ (screenshots in shots/); see sanctum.lua.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_sanctum
engine_prepare SANCTUM "$OUT" tools/ichor/tests/sanctum_consts.c tools/ichor/tests/sanctum_setup.s
# A few addresses the walk reads besides slice_symbols.sh's.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|CB2_UpdatePartyMenu)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/sanctum_symbols.lua"
engine_run SANCTUM "$OUT" tools/ichor/tests/sanctum.lua 600000 1800
