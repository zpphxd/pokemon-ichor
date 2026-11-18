#!/usr/bin/env bash
# Pan's Crook (WORLD_EXPLORATION §2): "Noon in Arkadia" played through (Krotos,
# the reeds, piping Pan awake, the Crook, the kid on the crag, the Kerazap), and
# climbing a face up and down on two maps: Arkadia's crag and Route 13's scarp.
#
#   tools/ichor/tests/crook_climb.sh [rom]     (default: pokeemerald.gba)
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_crook_climb
engine_prepare CROOK "$OUT" tools/ichor/tests/crook_climb_consts.c tools/ichor/tests/crook_climb_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia|Route13_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/crook_symbols.lua"
engine_run CROOK "$OUT" tools/ichor/tests/crook_climb.lua 400000 2000
