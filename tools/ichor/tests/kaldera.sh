#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
source tools/ichor/tests/engine_build.sh
OUT=build/test_kaldera
engine_prepare KALDERA "$OUT" tools/ichor/tests/kaldera_consts.c tools/ichor/tests/kaldera_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Kaldera[A-Za-z0-9_]*|Astyra_Harbor_EventScript_Mariner|TriremeDeck_EventScript_Nausikles|ElaiaVillage_PlayersHouse_1F_EventScript_(Mom|HoneyShelf))$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/kaldera_symbols.lua"
engine_run KALDERA "$OUT" tools/ichor/tests/kaldera.lua 240000 1000
