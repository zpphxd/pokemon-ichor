#!/usr/bin/env bash
# Assisted connected capital approach; not natural-level balance evidence.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_astyra
engine_prepare ASTYRA "$OUT" tools/ichor/tests/astyra_consts.c tools/ichor/tests/astyra_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route15_|Route16_|Daphni_|Astyra_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/astyra_symbols.lua"
engine_run ASTYRA "$OUT" tools/ichor/tests/astyra.lua 220000 1000
