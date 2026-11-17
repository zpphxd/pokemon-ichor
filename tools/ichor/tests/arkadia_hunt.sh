#!/usr/bin/env bash
# Assisted native Artemis trial and Laurel recovery, not balance approval.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_arkadia_hunt
engine_prepare HUNT "$OUT" tools/ichor/tests/arkadia_route_consts.c tools/ichor/tests/arkadia_route_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia_|EventScript_IchorTempleAltar_Artemis)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/hunt_symbols.lua"
engine_run HUNT "$OUT" tools/ichor/tests/arkadia_hunt.lua 250000 1200
