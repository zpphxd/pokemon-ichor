#!/usr/bin/env bash
# Assisted native return travel; not natural-level balance evidence.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_nemea
engine_prepare NEMEA "$OUT" tools/ichor/tests/nemea_consts.c tools/ichor/tests/nemea_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route13_|Route14_|Nemea_|Arkadia_|EmporionCity_EventScript_Nemea|EventScript_RockSmash)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/nemea_symbols.lua"
engine_run NEMEA "$OUT" tools/ichor/tests/nemea.lua 180000 900
