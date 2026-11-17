#!/usr/bin/env bash
# The Gulf rebuild (tools/ichor/maps/gulf.py): both seams of Route 9, Kirrha's
# hostel, the Korykian Cave (its brazier and Pan's niche), the bee errand, both
# ferry directions and Aigion's Homarion. Assisted travel; not balance evidence.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_gulf_walk
engine_prepare GULF "$OUT" tools/ichor/tests/gulf_walk_consts.c tools/ichor/tests/gulf_walk_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route9_|Kirrha|Aigion|GulfTrireme_|Lebadeia_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/gulf_symbols.lua"
engine_run GULF "$OUT" tools/ichor/tests/gulf_walk.lua 250000 1200
