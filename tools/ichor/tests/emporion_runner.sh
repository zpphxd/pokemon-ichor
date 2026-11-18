#!/usr/bin/env bash
# The road to Astyra after the Moon Laurel (Emporion's herm runner), in game.
#
#   tools/ichor/tests/emporion_runner.sh [rom]     (default: pokeemerald.gba; run make first)
#
# With Laurel 5, walks off Route 14's east end into Emporion by the Nemea Gate.
# Dromokleia's runner meets the player on the Nemea road, walks them to the
# travel herm and offers Eleusa. YES lands on Eleusa's herm tile, where the
# stood-aside watch names the east road. NO leaves the player at the herm, the
# runner waiting beside it; asking again re-offers, and the road's trigger stays
# spent. A player who lands at the herm instead hears it there. Screenshots are
# in build/test_emporion_runner/shots/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_emporion_runner
engine_prepare RUNNER "$OUT" tools/ichor/tests/emporion_runner_consts.c tools/ichor/tests/emporion_runner_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(EmporionCity_EventScript_HermRunner|EleusaVillage_EventScript_(WatchAside|Hoplite))[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/runner_symbols.lua"
engine_run RUNNER "$OUT" tools/ichor/tests/emporion_runner.lua 90000 600
