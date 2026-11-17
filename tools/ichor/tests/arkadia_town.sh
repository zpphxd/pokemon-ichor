#!/usr/bin/env bash
# The Arkadia cluster ported from claude/world-act2-0a92e7 onto main: every door
# in Arkadia, Styx Falls and Route 12 opens both ways, every seam crosses both
# ways, and the rooms' people hand over their gifts.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_arkadia_town
engine_prepare ARKADIATOWN "$OUT" tools/ichor/tests/arkadia_town_consts.c tools/ichor/tests/arkadia_town_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia|StyxFalls|Route12_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/arkadia_town_symbols.lua"
engine_run ARKADIATOWN "$OUT" tools/ichor/tests/arkadia_town.lua 600000 3000
