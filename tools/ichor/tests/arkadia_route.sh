#!/usr/bin/env bash
# Connected, assisted travel; not natural-level balance evidence.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_arkadia_route
engine_prepare APPROACH "$OUT" tools/ichor/tests/arkadia_route_consts.c tools/ichor/tests/arkadia_route_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route8_|Route9_|Route11_|Route12_|Lebadeia_|Kirrha_|Aigion_|GulfTrireme_|StyxFalls_|Arkadia_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/approach_symbols.lua"
engine_run APPROACH "$OUT" tools/ichor/tests/arkadia_route.lua 250000 1200
